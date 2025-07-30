import dataclasses
import json
import logging
import math
import os
import shutil
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import partial
from pathlib import Path
from typing import Any, Dict, Final, Optional, Tuple, Type, Union

import librosa
import numpy as np
import pandas as pd
import torch
import torch.distributed as dist
import torch.nn as nn
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.utils.data import DataLoader, Dataset, DistributedSampler
from torchinfo import summary
from tqdm import tqdm

from audiozen.accelerate import gather_object, get_world_size_and_rank, is_rank_zero, wait_for_everyone
from audiozen.logger import TensorboardLogger
from audiozen.optimization import (
    get_constant_schedule_with_warmup,
    get_cosine_with_min_lr_schedule_with_warmup,
    get_linear_schedule_with_warmup,
)
from audiozen.trainer_args import TrainingArgs
from audiozen.trainer_callback import CallbackHandler, StatefulTrainerCallback, TrainerCallback
from audiozen.trainer_utils import (
    collect_env,
    print_commandline_args,
)
from audiozen.utils import cleanup_before_training, log_header, prepare_dirs, set_random_seed


logger = logging.getLogger(__name__)

MODEL_NAME: Final = "model.pt"
OPTIMIZER_NAME: Final = "optimizer.pt"
SCHEDULER_NAME: Final = "scheduler.pt"
TRAIN_STATE_NAME: Final = "train_state.json"

OptimizerType = Optional[Tuple[Type[torch.optim.Optimizer], Dict[str, Any]]]


@dataclass
class TrainerState:
    """A dataclass to store the state of the trainer."""

    # Only set during training, will represent the epoch the training is at (the decimal part being the percentage of the current epoch completed).
    epochs_trained: int = 0
    steps_trained: int = 0
    early_stopping_patience_counter: int = 0

    best_score_epoch: int = 0

    # When tracking the best model, the value of the best metric encountered so far.
    best_metric: Optional[float] = None
    # When tracking the best model, the epoch at which the best model was encountered.
    best_model_epoch: Optional[int] = None
    # When tracking the best model, the value of the name of the checkpoint for the best model encountered so far.
    best_model_checkpoint: Optional[str] = None

    # The current ramp idx for pruning.
    prune_ramp_idx: Optional[int] = None

    def save_to_json(self, json_path: str | Path):
        """Save the content of this instance in JSON format inside `json_path`."""
        if isinstance(json_path, Path):
            json_path = str(json_path)
        json_string = json.dumps(dataclasses.asdict(self), indent=2, sort_keys=True) + "\n"
        with open(json_path, "w", encoding="utf-8") as f:
            f.write(json_string)

    @classmethod
    def load_from_json(cls, json_path: str | Path):
        """Create an instance from the content of `json_path`."""
        if isinstance(json_path, Path):
            json_path = str(json_path)

        with open(json_path, "r", encoding="utf-8") as f:
            text = f.read()
        return cls(**json.loads(text))


@dataclass
class TrainerControl:
    """
    A class that handles the `Trainer` control flow. This class is used by the `TrainerCallback` to activate some
    switches in the training loop.

    Args:
        should_training_stop (`bool`, *optional*, defaults to `False`):
            Whether or not the training should be interrupted. If `True`, this variable will not be set back to
            `False`. The training will just stop.
        should_evaluation_stop (`bool`, *optional*, defaults to `False`):
            Whether or not the evaluation should be interrupted. If `True`, this variable will be set back to
            `False` at the beginning of the next evaluation.
        should_epoch_stop (`bool`, *optional*, defaults to `False`):
            Whether or not the current epoch should be interrupted. If `True`, this variable will be set back to
            `False` at the beginning of the next epoch.
        should_save (`bool`, *optional*, defaults to `False`):
            Whether or not the model should be saved at this step. If `True`, this variable will be set back to `False`
            at the beginning of the next step.
        should_evaluate (`bool`, *optional*, defaults to `False`):
            Whether or not the model should be evaluated at this step. If `True`, this variable will be set back to
            `False` at the beginning of the next step.
        should_log (`bool`, *optional*, defaults to `False`):
            Whether or not the logs should be reported at this step. If `True`, this variable will be set back to
            `False` at the beginning of the next step.
    """

    should_evaluation_stop: bool = False

    # You can uncomment these lines if you want to use them in your Trainer class.
    # should_training_stop: bool = False
    # should_epoch_stop: bool = False
    # should_save: bool = False
    # should_evaluate: bool = False


class Trainer(ABC):
    """Trainer.

    Our intention is not to create a new complex Trainer class from scratch, which will be not helpful for the new
    users. Instead, we will create a simple Trainer class that is easy to understand if you are familiar with the
    Hugging Face Trainer API. We will also provide a lot of comments to help you understand the Trainer class.
    """

    def __init__(
        self,
        model: nn.Module,
        args: TrainingArgs,
        data_collator: Optional[Any] = None,
        train_dataset: Optional[Dataset] = None,
        eval_dataset: Optional[Union[Dataset, Dict[str, Dataset]]] = None,
        optimizer_cls_and_kwargs: OptimizerType = None,
        callbacks: Optional[list[TrainerCallback]] = None,
        **kwargs,
    ) -> None:
        """Initialize the Trainer.

        Args:
            model: The model to train, evaluate, or test.
            args: The training arguments. This is a dataclass that contains all the training arguments.
            data_collator: The data collator to use. Defaults to None.
            train_dataset: The training dataset. Defaults to None.
            eval_dataset: The evaluation dataset. Defaults to None. If can be a single or a dictionary of datasets.
            optimizer_cls_and_kwargs: The optimizer class and its keyword arguments. Defaults to None.
            **kwargs: Additional keyword arguments.

        Important attributes:
            in_training: Whether or not a model is currently running `train` (e.g. when `evaluate` is called while in
            `train`).
        """
        self.in_training = False
        # Set a flag tensor for early stopping and other breakpoints
        self.flag_tensor = None

        self.args = args

        # Set device as early as possible
        self.world_size, self.rank = get_world_size_and_rank()

        # Set random seed
        set_random_seed(seed=args.seed)

        # Datasets, model, optimizer, lr_scheduler
        self.data_collator = data_collator
        self.train_dataset = train_dataset

        # Dataloaders. They will be created in the `train` and `evaluate` methods.
        self.train_dataloader = None
        self.eval_dataloaders = None

        self.eval_dataset = eval_dataset
        self.model = model
        self.optimizer = None

        # Setup directories
        self._setup_exp_paths(output_dir=args.output_dir)

        # Acoustic parameters
        self._inject_acoustic_args()

        # Callbacks
        self.callback_handler = CallbackHandler(callbacks, trainer=self)

        # Trainer states
        self.state = TrainerState()

        # Trainer control
        self.control = TrainerControl()

        # Pandas settings for better display
        pd.set_option("display.float_format", lambda x: "%.3f" % x)

        if is_rank_zero():
            prepare_dirs([self.checkpoints_dir, self.tb_log_dir, self.enhanced_dir, self.metrics_dir])

            log_header("Environment Information")
            logger.info(f"\n{collect_env()}")

            log_header("Training Arguments")
            logger.info(print_commandline_args())

            self.writer = TensorboardLogger(self.tb_log_dir.as_posix())

            # Model summary
            log_header("Model Summary")
            logger.info(f"\n{summary(self.model, verbose=0)}")

        wait_for_everyone()

    @staticmethod
    def _search_latest_ckpt_path(checkpoints_dir: Path) -> Optional[Path]:
        """Find the latest checkpoint path from a given checkpoint directory.

        Args:
            checkpoints_dir: The directory where the checkpoints are saved.

        Returns:
            The latest checkpoint path. If no checkpoint is found, return None.
        """
        # Pick up all checkpoints with the format `epoch_*`
        checkpoints = sorted(checkpoints_dir.glob("epoch_" + ("[0-9]" * 4)))

        # Remove files that is not a checkpoint
        checkpoints = [ckpt for ckpt in checkpoints if ckpt.is_dir()]

        if len(checkpoints) == 0:
            if is_rank_zero():
                logger.info(
                    "You set `resume_from_checkpoint='latest'`, but no checkpoint is found. Will be treated as training from scratch."
                )
            return None

        # Pick up the latest checkpoint
        ckpt_path = checkpoints[-1]

        return ckpt_path

    def _parse_ckpt_path_or_alias(self, path_or_alias: str) -> Optional[Path]:
        """Parse the checkpoint path or alias.

        1. If the path_or_alias is "no", it means that the training starts from scratch. Returns None.
        2. If the path_or_alias is "latest", it means that the latest checkpoint is loaded. Returns the latest checkpoint
        path. In addition, if no checkpoint is found, it will be treated as training from scratch.
        3. If the path_or_alias is "best", it means that the best checkpoint is loaded. Returns the best checkpoint path.
        4. If the path_or_alias is a specific path, it means that the checkpoint is loaded from the specific path. Returns

        Args:
            path_or_alias: The checkpoint path or alias. It can be "no", "latest", "best", or a specific path.
        """
        if path_or_alias not in ["no", "latest", "best"] and not Path(path_or_alias).exists():
            raise FileNotFoundError(
                f"Checkpoint not found in {path_or_alias}. You can use 'no', 'latest', 'best', or a specific path."
            )

        ckpt_path = None

        if path_or_alias == "no":
            if is_rank_zero():
                logger.info("Training from scratch. No checkpoint is loaded.")
            return ckpt_path
        elif path_or_alias == "latest":
            ckpt_path = self._search_latest_ckpt_path(self.checkpoints_dir)

            if ckpt_path is None:
                # If no checkpoint is found, return None like "no"
                return ckpt_path
        elif path_or_alias == "best":
            ckpt_path = self.checkpoints_dir / "best"
        else:
            ckpt_path = Path(path_or_alias).expanduser().resolve()

        if not ckpt_path.exists():
            raise FileNotFoundError(f"Checkpoint not found in {ckpt_path.as_posix()}")

        return ckpt_path

    def _epoch_folder_name(self, epoch: int) -> str:
        assert epoch is not None, "Epoch is not provided."
        return f"epoch_{str(epoch).zfill(4)}"

    def _load_optimizer_and_scheduler(self, ckpt_path: Optional[Path] = None):
        if ckpt_path is None:
            return

        optimizer_state_fpath = ckpt_path / OPTIMIZER_NAME

        if optimizer_state_fpath.exists():
            assert self.optimizer is not None, "Optimizer is not initialized."
            optimizer_state = torch.load(optimizer_state_fpath, map_location="cpu", weights_only=True)
            self.optimizer.load_state_dict(optimizer_state)

            if is_rank_zero():
                logger.info(f"Optimizer checkpoint loaded from {optimizer_state_fpath}")

        scheduler_state_fpath = ckpt_path / SCHEDULER_NAME
        if scheduler_state_fpath.exists():
            assert self.lr_scheduler is not None, "LR scheduler is not initialized."
            scheduler_state = torch.load(scheduler_state_fpath, map_location="cpu", weights_only=True)
            self.lr_scheduler.load_state_dict(scheduler_state)

            if is_rank_zero():
                logger.info(f"Scheduler checkpoint loaded from {scheduler_state_fpath}")

    def _load_trainer_state(self, ckpt_epoch_dir: Optional[Path]) -> Optional[Dict[str, Any]]:
        """Load the trainer state from the checkpoint."""
        if ckpt_epoch_dir is None:
            return

        trainer_state_fpath = ckpt_epoch_dir / TRAIN_STATE_NAME
        if trainer_state_fpath.exists():
            self.state = TrainerState.load_from_json(trainer_state_fpath)

            if is_rank_zero():
                logger.info(f"Trainer state loaded from {trainer_state_fpath}")
                logger.info(f"Trainer state: {self.state}")

    def _load_stateful_callback(self, ckpt_epoch_dir: Optional[Path]):
        """Load the stateful callbacks from the checkpoint."""
        if ckpt_epoch_dir is None:
            return

        for i, cb in enumerate(self.callback_handler.callbacks):
            if isinstance(cb, StatefulTrainerCallback):
                # Use `class_name` and `i` to avoid when multiple callbacks of the same class are used.
                state_dict_fpath = ckpt_epoch_dir / f"{cb.__class__.__name__}_{i}.state_dict.json"

                if state_dict_fpath.exists():
                    state_dict = json.load(open(state_dict_fpath, "r", encoding="utf-8"))
                    cb.load_state_dict(state_dict)

                    if is_rank_zero():
                        logger.info(f"Stateful callback {cb.__class__.__name__} loaded from {state_dict_fpath}")

    def _prepare_ddp_model(self, model):
        """Prepare the model for acceleration.

        Note:
            You should never try to change your model's parameters after wrapping up your model with DDP. Because, when
            wrapping up your model with DDP, the constructor of DDP will register the additional gradient reduction
            functions on all the parameters of the model itself at time of construction. If you change the parameters
            of the model after wrapping up the model with DDP, the gradient reduction functions will not be matched
            with the correct parameters of the model. It means that you must load the model's weights before wrapping
            up the model with DDP. See:
            https://pytorch.org/docs/stable/generated/torch.nn.parallel.DistributedDataParallel.html

        Args:
            model: The model to prepare.

        Returns:
            The model prepared for acceleration.
        """
        if dist.is_available() and dist.is_initialized():
            model = model.to(self.rank)
            model = DDP(model, find_unused_parameters=self.args.ddp_find_unused_parameters)
            # synchronize before training begins
            dist.barrier()
            return model
        else:
            model = model.to("cpu")
            return model

    @staticmethod
    def _current_time_now():
        return time.strftime("%Y_%m_%d--%H_%M_%S")

    def _setup_exp_paths(self, output_dir: str):
        """Set the paths for the experiment.

        Args:
            output_dir: the root directory to save all experiments.

        Example:
            - output_dir: /home/xhao/exp/fullsubnet_lr_0.g
            - checkpoints_dir: /home/xhao/exp/fullsubnet_lr_0.1/checkpoints
            - tb_log_dir: /home/xhao/exp/fullsubnet_lr_0.1/tb_log
            - enhanced_dir: /home/xhao/exp/fullsubnet_lr_0.1/enhanced
            - metrics_dir: /home/xhao/exp/fullsubnet_lr_0.1/metrics
            - source_code_backup_dir: /home/xhao/exp/fullsubnet_lr_0.1/source_code__YYYY_MM_DD__HH_MM_SS
            - model_args_path: /home/xhao/exp/fullsubnet_lr_0.1/model_args__YYYY_MM_DD__HH_MM_SS.yaml
        """
        time_now = self._current_time_now()  # returns a timestamp string

        self.output_dir = Path(output_dir).expanduser().absolute()
        self.checkpoints_dir = self.output_dir / "checkpoints"
        self.tb_log_dir = self.output_dir / "tb_log"
        self.enhanced_dir = self.output_dir / "enhanced"
        self.metrics_dir = self.output_dir / "metrics"

        # Each run will have a unique source code, config, and log file.
        self.source_code_dir = Path(__file__).expanduser().absolute().parent.parent.parent
        self.source_code_backup_dir = self.output_dir / f"source_code__{time_now}"
        self.model_args_path = self.output_dir / f"model_args__{time_now}.yaml"
        self.loss_log_path = self.output_dir / "loss.csv"

    def _inject_acoustic_args(self):
        """Setup acoustic arguments."""
        n_fft = self.args.acoustic_n_fft
        hop_length = self.args.acoustic_hop_length
        win_length = self.args.acoustic_win_length
        sr = self.args.acoustic_sr

        # Support for torch and librosa stft
        self.torch_stft = partial(torch.stft, n_fft=n_fft, hop_length=hop_length, win_length=win_length)
        self.torch_istft = partial(torch.istft, n_fft=n_fft, hop_length=hop_length, win_length=win_length)
        self.librosa_stft = partial(librosa.stft, n_fft=n_fft, hop_length=hop_length, win_length=win_length)
        self.librosa_istft = partial(librosa.istft, n_fft=n_fft, hop_length=hop_length, win_length=win_length)

        self.n_fft = n_fft
        self.hop_length = hop_length
        self.win_length = win_length
        self.sr = sr

    def set_models_to_train_mode(self):
        """Set models to train mode.

        You can override this method to set your own models to train mode. For example, in GAN training, you may want
        to set the generator and the discriminator to train mode.
        """
        self.model.train()

    def set_models_to_eval_mode(self):
        self.model.eval()

    def lr_scheduler_step(self):
        """Step the lr scheduler.

        You can override this method to step your own lr scheduler. For example, in GAN training, you may want to step
        the lr scheduler of the generator and the discriminator.
        """
        self.lr_scheduler.step()

    def create_bar_desc(self, loss_dict: Dict[str, float]):
        bar_desc = ""
        for k, v in loss_dict.items():
            bar_desc += f"{k}: {(v):.4f}, "
        bar_desc += f"lr: {self.lr_scheduler.get_last_lr()[-1]:.10f}"

        if self.args.plot_lr:
            self.writer.add_scalar("Train_Step/lr", self.lr_scheduler.get_last_lr()[-1], self.state.steps_trained)

        return bar_desc

    @staticmethod
    def _get_model_state_dict(model: nn.Module) -> Dict[str, Any]:
        """Get the model state dict. Compatible with DDP and non-DDP models."""
        if isinstance(model, DDP):
            logger.info("Extract the `state_dict` from the `model.module.state_dict()`...")
            model_state = model.module.state_dict()
        else:
            logger.info("Extract the `state_dict` from the `model.state_dict()`...")
            model_state = model.state_dict()

        return model_state

    def _load_model(self, ckpt_epoch_dir: Optional[Path]) -> Optional[Dict[str, Any]]:
        """Load the model state and trainer state from the checkpoint."""
        if ckpt_epoch_dir is None:
            # We have warnings in the `_parse_ckpt_path_or_alias` method. Don't worry about here.
            return

        model_state_fpath = ckpt_epoch_dir / MODEL_NAME
        if model_state_fpath.exists():
            model_state = torch.load(model_state_fpath, map_location="cpu", weights_only=True)
            self.model.load_state_dict(model_state)

            if is_rank_zero():
                logger.info(f"Model checkpoint loaded from {model_state_fpath}")

    def _save_model(self, ckpt_epoch_dir: Path):
        """Save the model."""
        model_state = self._get_model_state_dict(self.model)

        model_state_fpath = ckpt_epoch_dir / MODEL_NAME
        torch.save(model_state, model_state_fpath)

        logger.info(
            f"Model checkpoint {os.path.getsize(model_state_fpath) / 1000**3:.2f} GB saved to {model_state_fpath}"
        )

    def _save_trainer_state(self, ckpt_epoch_dir: Path):
        """Save the trainer state."""
        trainer_state_fpath = ckpt_epoch_dir / TRAIN_STATE_NAME
        self.state.save_to_json(trainer_state_fpath)

        logger.info(f"Trainer state saved to {trainer_state_fpath}")

    def _save_stateful_callback(self, ckpt_epoch_dir: Path):
        """Save the stateful callbacks to the checkpoint directory."""
        for i, cb in enumerate(self.callback_handler.callbacks):
            if isinstance(cb, StatefulTrainerCallback):
                # Use `class_name` and `i` to avoid when multiple callbacks of the same class are used.
                state_dict_fpath = ckpt_epoch_dir / f"{cb.__class__.__name__}_{i}.state_dict.json"
                state_dict = cb.state_dict()
                json.dump(state_dict, open(state_dict_fpath, "w", encoding="utf-8"), indent=2)

                if is_rank_zero():
                    logger.info(f"Stateful callback {cb.__class__.__name__} saved to {state_dict_fpath}")

    def _save_optimizer_and_scheduler(self, ckpt_epoch_dir: Path):
        """Save the optimizer and the learning rate scheduler."""
        optimizer_state_fpath = ckpt_epoch_dir / OPTIMIZER_NAME
        scheduler_state_fpath = ckpt_epoch_dir / SCHEDULER_NAME

        if self.optimizer is not None:
            optimizer_state_fpath = ckpt_epoch_dir / OPTIMIZER_NAME
            torch.save(self.optimizer.state_dict(), optimizer_state_fpath)
            logger.info(
                f"Optimizer checkpoint {os.path.getsize(optimizer_state_fpath) / 1000**3:.2f} GB saved to {optimizer_state_fpath}"
            )

        if self.lr_scheduler is not None:
            scheduler_state_fpath = ckpt_epoch_dir / SCHEDULER_NAME
            torch.save(self.lr_scheduler.state_dict(), scheduler_state_fpath)
            logger.info(
                f"Scheduler checkpoint {os.path.getsize(scheduler_state_fpath) / 1000**3:.2f} GB saved to {scheduler_state_fpath}"
            )

    def _save_checkpoint(self, epoch: int):
        """Save the checkpoint.

        It will only be saved on the rank zero process.

        Args:
            epoch: The current epoch.
            is_best_epoch: Whether the current epoch is the best epoch. Defaults to False.
        """
        if not is_rank_zero():
            return

        # Find all checkpoints
        checkpoints = sorted(self.checkpoints_dir.glob("epoch_" + ("[0-9]" * 4)))
        if epoch < len(checkpoints):
            logger.warning(
                f"Current epoch is {epoch}, but found {len(checkpoints)} checkpoints. "
                f"This may be caused by you running the same experiment multiple times. "
                f"Recommend to run the experiment with a different `output_dir`."
                f"Otherwise, the newer checkpoints will be removed."
            )

        # Remove the old checkpoints
        if len(checkpoints) > self.args.save_total_limit:
            logger.info(
                f"Found {len(checkpoints)} checkpoints, keeping the latest {self.args.save_total_limit} checkpoints."
            )

            for checkpoint_dir in checkpoints[: -self.args.save_total_limit]:
                shutil.rmtree(checkpoint_dir.as_posix())
                logger.info(f"Checkpoint {checkpoint_dir.as_posix()} is removed.")

        ckpt_epoch_dir = self.checkpoints_dir / self._epoch_folder_name(epoch)
        ckpt_epoch_dir.mkdir(parents=True, exist_ok=True)

        self._save_model(ckpt_epoch_dir)
        self._save_trainer_state(ckpt_epoch_dir)
        self._save_stateful_callback(ckpt_epoch_dir)
        self._save_optimizer_and_scheduler(ckpt_epoch_dir)

    def _should_early_stop(self, metric: float):
        should_stop = False

        operator = np.greater if self.args.greater_is_better else np.less

        if self.state.best_metric is None or operator(metric, self.state.best_metric):
            self.state.best_metric = metric
            self.state.best_model_epoch = self.state.epochs_trained
            self.state.best_model_checkpoint = (
                self.checkpoints_dir / self._epoch_folder_name(self.state.epochs_trained)
            ).as_posix()
            self.state.early_stopping_patience_counter = 0
            logger.info(f"Found new best score: {metric:.4f}, saving checkpoint...")
        else:
            logger.info("Current model did not improve from the best model.")
            logger.info(f"\t Current metric: {metric:.4f} at epoch {self.state.epochs_trained}.")
            logger.info(f"\t Best metric: {self.state.best_metric:.4f} at epoch {self.state.best_model_epoch}.")
            self.state.early_stopping_patience_counter += 1
            logger.info(
                f"Early stopping counter: {self.state.early_stopping_patience_counter} out of {self.args.early_stopping_patience}"
            )

            if self.state.early_stopping_patience_counter >= self.args.early_stopping_patience:
                logger.info("Early stopping triggered, stopping training...")
                should_stop = True

        return should_stop

    def get_train_dataloader(self):
        if self.train_dataset is None:
            raise ValueError("Trainer: `train()` requires a `train_dataset`.")

        if dist.is_available() and dist.is_initialized():
            sampler = DistributedSampler(
                self.train_dataset,
                num_replicas=self.world_size,
                rank=self.rank,
                shuffle=True,
                seed=0,  # This number should be identical across all processes in the distributed group
            )
        else:
            sampler = None

        dataloader_params = {
            "batch_size": self.args.per_device_train_batch_size,
            "collate_fn": self.data_collator,
            "num_workers": self.args.dataloader_num_workers,
            "pin_memory": self.args.dataloader_pin_memory,
            "persistent_workers": self.args.dataloader_persistent_workers,
            "drop_last": self.args.dataloader_drop_last,
            "prefetch_factor": self.args.dataloader_prefetch_factor,
            "sampler": sampler,
            "shuffle": (sampler is None),
        }

        if is_rank_zero():
            logger.info("Dataset and Sampler are initialized.")

        return DataLoader(self.train_dataset, **dataloader_params)

    def create_eval_dataloaders(self) -> Dict[str, DataLoader]:
        """Create the evaluation dataloaders.

        If the eval_dataset is a single dataset, it will be converted to a dictionary with the key "default".

        Returns:
            eval_dataloaders: the evaluation dataloaders.
        """
        if self.eval_dataset is None:
            raise ValueError("Trainer: evaluation requires a `eval_dataset`.")

        eval_dataset = self.eval_dataset
        data_collator = self.data_collator

        if not isinstance(eval_dataset, dict):
            if isinstance(eval_dataset, Dataset):
                eval_dataset = {"default": eval_dataset}
            else:
                raise ValueError("Trainer: `eval_dataset` should be either a dataset or a dictionary of datasets.")

        dataloader_params = {
            "batch_size": self.args.eval_batch_size,
            "collate_fn": data_collator,
            "num_workers": self.args.dataloader_num_workers,
            "pin_memory": self.args.dataloader_pin_memory,
            "persistent_workers": self.args.dataloader_persistent_workers,
            # Keep last batch during evaluation for dataset integrity. If sample count isn't divisible by batch size,
            # DistributedSampler pads last batch by wrapping around. Extra samples can be removed when calculating
            # metric means in evaluation_epoch_end.
            "drop_last": False,
            "prefetch_factor": self.args.dataloader_prefetch_factor,
            "shuffle": False,  # No need to shuffle for evaluation
        }

        eval_dataloaders = {}
        for key, dataset in eval_dataset.items():
            if dist.is_available() and dist.is_initialized():
                sampler = DistributedSampler(
                    dataset,
                    num_replicas=self.world_size,
                    rank=self.rank,
                    shuffle=False,  # No need to shuffle for evaluation
                    seed=0,  # This number should be identical across all processes in the distributed group
                )
            else:
                sampler = None

            eval_dataloaders[key] = DataLoader(
                dataset=dataset,
                sampler=sampler,
                **dataloader_params,
            )

        if is_rank_zero():
            logger.info("Evaluation dataloaders are initialized.")
            logger.info(f"Number of evaluation dataloaders: {len(eval_dataloaders)}")

        return eval_dataloaders

    @staticmethod
    def get_optimizer_cls_and_kwargs(args: TrainingArgs) -> Tuple[Type[torch.optim.Optimizer], Dict[str, Any]]:
        """Returns the optimizer class and optimizer parameters based on the training arguments."""
        optimizer_kwargs = {"lr": args.learning_rate}

        adam_kwargs = {"betas": (args.adam_beta1, args.adam_beta2), "eps": args.adam_epsilon}

        if args.optim == "adamw":
            optimizer_cls = torch.optim.AdamW
            optimizer_kwargs |= adam_kwargs
        elif args.optim == "adam":
            optimizer_cls = torch.optim.Adam
            optimizer_kwargs |= adam_kwargs
        else:
            raise ValueError(f"Unknown optimizer: {args.optim}")

        return optimizer_cls, optimizer_kwargs

    def create_optimizer(self):
        if self.optimizer is None:
            optimizer_cls, optimizer_kwargs = self.get_optimizer_cls_and_kwargs(self.args)
            self.optimizer = optimizer_cls(self.model.parameters(), **optimizer_kwargs)

    def get_warmup_steps(self, warmup_steps, max_steps, warmup_ratio):
        """Calculate the number of warmup steps based on the training arguments."""
        if warmup_steps > 0:
            if is_rank_zero():
                logger.info(f"warmup_steps={warmup_steps}. warmup_ratio will be ignored.")
            return warmup_steps
        else:
            return math.ceil(max_steps * warmup_ratio)

    def create_warmup_scheduler(self, optimizer, scheduler_name, max_steps: int):
        num_warmup_steps = self.get_warmup_steps(self.args.warmup_steps, max_steps, self.args.warmup_ratio)

        if scheduler_name == "constant_schedule_with_warmup":
            return get_constant_schedule_with_warmup(optimizer=optimizer, num_warmup_steps=num_warmup_steps)
        elif scheduler_name == "linear_schedule_with_warmup":
            return get_linear_schedule_with_warmup(
                optimizer=optimizer, num_warmup_steps=num_warmup_steps, num_training_steps=max_steps
            )
        elif scheduler_name == "cosine_with_min_lr_schedule_with_warmup":
            return get_cosine_with_min_lr_schedule_with_warmup(
                optimizer=optimizer,
                num_warmup_steps=num_warmup_steps,
                num_training_steps=max_steps,
                num_cycles=self.args.cosine_with_min_lr_schedule_with_warmup_num_cycles,
                initial_lr=self.args.cosine_with_min_lr_schedule_with_warmup_initial_lr,
                min_lr=self.args.cosine_with_min_lr_schedule_with_warmup_min_lr,
            )
        else:
            raise ValueError(f"Invalid scheduler name: {scheduler_name}")

    def create_scheduler(self, max_steps: int, scheduler_specific_kwargs: Optional[Dict] = None):
        """Setup the learning rate scheduler.

        You can override this method to create your own schedulers. For example, in GAN training, you may want to
        create two schedulers for the generator and the discriminator.

        Args:
            max_steps: the maximum number of steps to train.
        """
        self.lr_scheduler = self.create_warmup_scheduler(
            optimizer=self.optimizer, scheduler_name=self.args.lr_scheduler_type, max_steps=max_steps
        )

    def create_optimizer_and_scheduler(self, max_steps: int):
        """Setup the optimizer and the learning rate scheduler.

        We provide a reasonable default that works well. If you want to use something else, you can pass a tuple in the
        Trainer's init through `optimizers`, or subclass and override this method (or `create_optimizer` and/or
        `create_scheduler`) in a subclass.
        """
        self.create_optimizer()
        self.create_scheduler(max_steps=max_steps)

    def set_trigger(self):
        """Sets the internal trigger tensor to 1 on the current process. A latter check should follow using this which
        will check across all processes.

        Notes:
            Does not require `wait_for_everyone()`
        """
        if dist.is_available() and dist.is_initialized():
            self.flag_tensor = torch.tensor(1, device=self.rank)

    def check_trigger(self):
        """Checks if the internal trigger tensor has been set to 1 in any of the processes. If so, will return `True`
        and reset the trigger tensor to 0.

        Notes:
            Requires `wait_for_everyone()`
        """
        if dist.is_available() and dist.is_initialized():
            # Make sure that all processes have set the trigger tensor
            # Now that we are outside `__init__`, we can initialize it if it is `None` on device
            if self.flag_tensor is None:
                self.flag_tensor = torch.tensor(0, device=self.rank)

            dist.all_reduce(self.flag_tensor, op=dist.ReduceOp.SUM)

            if self.flag_tensor.item() >= 1:
                self.flag_tensor = torch.tensor(0, device=self.rank)
                return True

            return False

    def train(self):
        """Main training entry point."""
        self.in_training = True

        # Load the model state before wrapping up the model with DDP according to the PyTorch documentation
        ckpt_path = self._parse_ckpt_path_or_alias(self.args.resume_from_checkpoint)
        self._load_trainer_state(ckpt_path)
        self._load_stateful_callback(ckpt_path)
        self._load_model(ckpt_path)

        cleanup_before_training()

        # Initialize the training dataloader
        train_dataloader = self.get_train_dataloader()

        # Setting up training control variables
        num_update_steps_per_epoch = len(train_dataloader)  # #samples // batch_size // world_size
        num_update_steps_per_epoch = num_update_steps_per_epoch // self.args.gradient_accumulation_steps
        num_update_steps_per_epoch = max(num_update_steps_per_epoch, 1)
        if self.args.max_steps > 0:
            # max_steps is set, so we need to calculate the number of epochs based on max_steps
            max_steps = self.args.max_steps
            num_train_epochs = max_steps // num_update_steps_per_epoch + int(
                max_steps % num_update_steps_per_epoch > 0
            )
        else:
            num_train_epochs = self.args.num_train_epochs
            max_steps = math.ceil(num_train_epochs * num_update_steps_per_epoch)

        # Prepare the model for DDP
        self.model = self._prepare_ddp_model(self.model)

        # Create optimizer and lr_scheduler
        # Make sure that the optimizer and lr_scheduler are created after the model is wrapped up with DDP
        self.create_optimizer_and_scheduler(max_steps=max_steps)
        self._load_optimizer_and_scheduler(ckpt_path)

        # Train!!!
        if is_rank_zero():
            log_header("Training Arguments")
            logger.info(f"`epochs_trained` = {self.state.epochs_trained}")
            logger.info(f"Num Epochs = {num_train_epochs:,}")
            logger.info(f"`steps_per_epoch` = {num_update_steps_per_epoch:,}")
            logger.info(f"Instantaneous batch size per device = {self.args.per_device_train_batch_size:,}")
            logger.info(f"Gradient Accumulation steps = {self.args.gradient_accumulation_steps}")
            logger.info(f"Total optimization steps = {max_steps:,}")

        self.control = self.callback_handler.on_train_begin(self.control)

        for epoch in range(self.state.epochs_trained + 1, num_train_epochs + 1):
            # TODO You may use `ProgressCallback` to track the progress of training.

            if is_rank_zero():
                log_header(f"Epoch {epoch} out of {num_train_epochs}")
                logger.info("Begin training...")

            if dist.is_available() and dist.is_initialized():
                train_dataloader.sampler.set_epoch(epoch)  # type: ignore

            self.set_models_to_train_mode()

            training_epoch_output = []

            # The iter number of progress bar increments by 1 by default whether gradient accumulation is used or not.
            # but we update the description of the progress bar only when the gradients are synchronized across all
            # processes.
            dataloader_bar = tqdm(
                train_dataloader,
                desc="",
                dynamic_ncols=True,
                bar_format="{l_bar}{r_bar}",
                colour="green",
                disable=not is_rank_zero(),
                position=0,
                leave=True,
            )

            for batch_idx, batch in enumerate(dataloader_bar):
                # You are responsible for calling `.backward()`, `.step()`, and `.zero_grad()` in your implementation
                loss_dict = self.training_step(batch, batch_idx)
                training_epoch_output.append(loss_dict)
                if is_rank_zero():
                    bar_desc = self.create_bar_desc(loss_dict)
                    dataloader_bar.set_description_str(bar_desc)

                self.lr_scheduler_step()
                self.state.steps_trained += 1
            self.state.epochs_trained += 1

            # Clean cache
            # [Not necessary in most cases]
            # Normally, PyTorch will occupy maximum GPU memory after training for a while. This will prevent other
            # processes from other users from using the GPU. It is a safe practice. Tt keeps it in a pool so that next
            # allocations can be done much faster. However, we need to use more memeroy during evaluation (DNSMOS), so
            # we need to clean the cache.
            torch.cuda.empty_cache()

            # Hook `training_epoch_end`
            self.training_epoch_end(training_epoch_output)

            # Should save?
            if is_rank_zero() and epoch % self.args.save_epoch_interval == 0:
                self._save_checkpoint(epoch=epoch)

            # Should evaluate?
            if epoch % self.args.eval_epoch_interval == 0:
                if is_rank_zero():
                    logger.info("Training finished, begin evaluation...")

                with torch.no_grad():
                    # only the main process will receive the score
                    score = self.evaluate()
                    if is_rank_zero():
                        should_stop = self._should_early_stop(score)
                        if should_stop:
                            self.set_trigger()

                if is_rank_zero():
                    logger.info("Evaluation finished.")

            wait_for_everyone()

            # Check if any process has set the trigger tensor
            if self.check_trigger():
                break

    @torch.no_grad()
    def evaluate(self):
        """Run evaluation (validation) and return metrics.

        This method evaluates the model on validation datasets and calculates performance metrics.

        Note:
            The method operates in two distinct modes:
            1. During training (`in_training=True`):
               - Uses the already-loaded model and existing DDP setup
               - Logs metrics to TensorBoard for tracking progress
               - Metrics influence early stopping decisions

            2. Standalone evaluation (`in_training=False`):
               - Automatically loads the model from specified checkpoint
               - Sets up DDP for distributed evaluation
               - Saves metrics to files but doesn't log to TensorBoard

        Process Flow:
            1. Initializes evaluation dataloaders if not already created
            2. For standalone mode: loads checkpoint and prepares DDP model
            3. Runs evaluation loop across all validation datasets
            4. Gathers results from all distributed processes
            5. Calculates and logs aggregate metrics

        Returns:
            float: A single representative metric score for model comparison and early stopping.
               Returns 0.0 for non-zero ranks in distributed settings.

        See Also:
            `predict()`: Similar method for test-time inference which don't require ground truth labels.
            `evaluation_loop()`: Core implementation shared between evaluation and prediction
        """
        if is_rank_zero():
            logger.info("Begin evaluation...")

        # init_eval_dataloaders() might be called multiple times if the evaluation is called during training.
        # Here, we will make sure that the dataloaders are only prepared once.
        if self.eval_dataloaders is None:
            if is_rank_zero():
                logger.info("The evaluation dataloaders are not initialized. Initialize them now...")
            self.eval_dataloaders = self.create_eval_dataloaders()

        # If the current run is not in training (doesnot use train mode), we need to prepare load the model
        if not self.in_training:
            # Load checkpoint before setting up the model
            ckpt_path = self._parse_ckpt_path_or_alias(self.args.resume_from_checkpoint)

            # Load the model state before wrapping up the model with DDP according to the PyTorch documentation
            self._load_model(ckpt_path)
            self._load_trainer_state(ckpt_path)

            # Prepare the model for DDP
            if is_rank_zero():
                logger.info("Prepare the model for DDP...")

            self.model = self._prepare_ddp_model(self.model)

        self.control = self.callback_handler.on_evaluation_begin(self.control)

        if self.control.should_evaluation_stop:
            if is_rank_zero():
                logger.info("Evaluation stopped by the callback handler.")
            return 0.0

        evaluation_output = self.evaluation_loop(description="evaluate", gather_step_output=True)

        if is_rank_zero():
            # only the main process will run evaluation_epoch_end
            logger.info("Evaluation finished, begin hook `evaluation_epoch_end`...")

            log_to_tensorboard = True if self.in_training else False
            score = self.evaluation_epoch_end(evaluation_output, log_to_tensorboard=log_to_tensorboard)

            return score
        else:
            return 0.0

    @torch.no_grad()
    def predict(self):
        """Run prediction.

        In the predict mode, the model will be loaded from a checkpoint and the evaluation_loop will be called.
        However, the evaluation_loop will not gather any step_output from all processes.
        """
        if is_rank_zero():
            logger.info("Begin predicting...")

        # In the predict mode, get_eval_dataloaders() will be called only once.
        self.eval_dataloaders = self.create_eval_dataloaders()

        # Load checkpoint before setting up the model
        ckpt_path = self._parse_ckpt_path_or_alias(self.args.resume_from_checkpoint)
        self._load_model(ckpt_path)
        self._load_trainer_state(ckpt_path)

        # Prepare the model for DDP
        if is_rank_zero():
            logger.info("Prepare the model for DDP...")

        self.model = self._prepare_ddp_model(self.model)

        # In the predict mode, we don't need to gather the step_output from all processes.
        self.evaluation_loop(description="predict", gather_step_output=False)

        logger.info("Prediction finished.")

    @torch.no_grad()
    def evaluation_loop(self, description: str, gather_step_output: bool = False):
        """Runs the prediction/evaluation loop for all evaluation dataloaders.

        This method is shared by `Trainer.evaluate()` and `Trainer.predict()`. It sets models to
        evaluation mode, then iterates through all evaluation dataloaders, collecting
        outputs from each batch using the `evaluation_step` method.

        Args:
            description (str): A string describing the evaluation run, used for logging.
            gather_step_output (bool, optional): If True, outputs from all processes are gathered
                on process 0 during distributed training. Defaults to False.

        Returns:
            dict: A nested dictionary containing evaluation outputs organized by dataloader ID:
                {
                    "dataloader_id_1": [
                        [{"metric_1": 0.95, "metric_2": 0.87, ...}, {...}, ...],  # Batch 1 results
                        [{"metric_1": 0.92, "metric_2": 0.83, ...}, {...}, ...],  # Batch 2 results
                        ...
                    ],
                    "dataloader_id_2": [
                        [...],  # Batch 1 results
                        [...],  # Batch 2 results
                        ...
                    ],
                    ...
                }

            You may need to **flatten** the output.


        Note:
            - The method follows best practices by computing metrics during the evaluation step
              rather than at the end, which helps prevent memory overflow and enables early error
              detection.
            - When `gather_step_output=True`, results from all processes are collected on the
              main process, which is useful for distributed training scenarios.

        See Also:
            - `Trainer.evaluate()`: Calls this method for evaluation with ground truth labels.
            - `Trainer.predict()`: Calls this method for prediction without ground truth labels.
            - `Trainer.evaluation_epoch_end()`: Processes the outputs after the evaluation loop.
        """
        args = self.args

        self.set_models_to_eval_mode()

        if is_rank_zero():
            logger.info(f"***** Running {description} *****")
            logger.info(f"  Batch size = {args.eval_batch_size}")

        evaluation_output = {}
        assert self.eval_dataloaders is not None, "The evaluation dataloaders are not initialized."
        for dl_idx, (dl_id, dataloader) in enumerate(self.eval_dataloaders.items()):
            dataloader_output = []
            for batch_idx, batch in enumerate(
                tqdm(
                    dataloader,
                    desc=f"Evaluation on dataloader `{dl_id}`",
                    bar_format="{l_bar}{r_bar}",
                    dynamic_ncols=True,
                    disable=not is_rank_zero(),
                )
            ):
                """
                Best practices for metric computation in evaluation:

                1. Calculate metrics directly in `evaluation_step` rather than `evaluation_epoch_end` because:
                   - Most evaluation metrics are sequential and not parallelizable
                   - Prevents memory overflow when handling large datasets in distributed settings
                   - Enables earlier error detection in metric computation code
                   - Provides more granular insights into per-sample performance

                2. Implementation strategy:
                   - Compute metrics immediately for each batch in this step
                   - Return structured dictionaries with metric values
                   - Handle any necessary normalization here
                   - Use `evaluation_epoch_end` only for aggregation and reporting

                3. For distributed evaluation:
                   - Each process computes metrics on its own batch portion
                   - Results are gathered and combined afterward
                   - This approach scales better with dataset size
                """
                with torch.no_grad():
                    step_output = self.evaluation_step(batch, batch_idx, dl_id)

                # If `gather_step_output` is True, we will gather the step_output from all processes and return a list
                # of all metric scores.
                if gather_step_output:
                    """Gather step outputs from all processes into a single list on the main process.

                    For example, with 2 processes evaluating 2 samples each, the result becomes:
                    step_output = [
                        {"metric_1": 0.95, "metric_2": 0.87, ...},  # sample 1 from process 0
                        {"metric_1": 0.92, "metric_2": 0.82, ...},  # sample 1 from process 1
                        {"metric_1": 0.91, "metric_2": 0.85, ...},  # sample 2 from process 0
                        {"metric_1": 0.89, "metric_2": 0.81, ...},  # sample 2 from process 1
                    ]

                    This concatenated list preserves the original batch order across processes,
                    which is essential for proper metric calculation in distributed evaluation.
                    """
                    step_output = gather_object(step_output, dst=0)
                dataloader_output.append(step_output)
            evaluation_output[dl_id] = dataloader_output

        """
        `evaluation_output` structure:
        {
            "dataloader_id_1": [
                [{"metric_1": 0.95, "metric_2": 0.87, ...}, {...}],  # Batch 1 results
                [{"metric_1": 0.92, "metric_2": 0.83, ...}, {...}],  # Batch 2 results
                ...
            ],
            "dataloader_id_2": [
                [...],  # Batch 1 results
                [...],  # Batch 2 results
                ...
            ],
            ...
        }

        Where each inner list contains metric dictionaries for each sample in the batch,
        gathered across all processes when using distributed training.
        """
        return evaluation_output

    @abstractmethod
    def training_step(self, batch, batch_idx):
        """Implement a training step (iteration).

        Implement your own training step here. The input batch is from a training dataloader and the output of this
        function can be various. For example, it can be a dict of loss, or a dict of loss and some enhanced audio
        signals. Here is the persuade code for training a model:

        .. code-block:: python
            :emphasize-lines: 6

            for epoch in range(start_epoch, end_epoch):
                self.model.train()

                training_epoch_output = []
                for batch, batch_index in dataloader:
                    loss_dict = training_step(batch, batch_idx)
                    training_epoch_output.append(loss_dict)

                training_epoch_end(training_epoch_output)
                save_checkpoint()
                if some_condition:
                    score = validate()
                    if score > best_score:
                        save_checkpoint(best=True)

        Args:
            batch: a batch of data, which passed from a custom training dataloader.
            batch_idx: the index of the current batch.

        Returns:
            loss_dict: a dict of loss. For example, {"loss_1": loss, "loss_2": loss, ...}
        """
        raise NotImplementedError

    def training_epoch_end(self, training_epoch_output):
        """Implement the logic of the end of a training epoch.

        By default, this function will log the mean loss of each loss item on a training epoch. You can override this.
        When the training epoch ends, this function will be called. The input is a list of the loss dict of each step
        in a training epoch. You may want to log the epoch-level training loss here.

        Examples:

        ```
        for epoch in range(start_epoch, end_epoch):
            self.model.train()

            training_epoch_output = []
            for batch, batch_index in dataloader:
                loss = training_step(batch, batch_idx)
                training_epoch_output.append(loss)

            training_epoch_end(training_epoch_output)
            save_checkpoint()
            if some_condition:
                score = validate()
                if score > best_score:
                    save_checkpoint(best=True)
        ```

        Args:
            training_epoch_output: the output of the training epoch. It may a list of the output of each batch
            (iteration).
        """
        # Compute mean loss on all loss items on a epoch
        if is_rank_zero():
            loss_keys = training_epoch_output[0].keys()
            loss_dict = {key: np.mean([step_out[key] for step_out in training_epoch_output]) for key in loss_keys}

            for key, value in loss_dict.items():
                logger.info(f"Loss '{key}' on epoch {self.state.epochs_trained}: {value}")
                self.writer.add_scalar(f"Train_Epoch/{key}", value, self.state.epochs_trained)

            # loss_dict["epoch"] = self.state.epochs_trained
            # Append the loss to the loss log
            # df = pd.DataFrame(loss_dict, index=[0])
            # df.to_csv(self.loss_log_path, mode="a", index=False, header=not self.loss_log_path.exists())

    @abstractmethod
    def evaluation_step(self, batch, batch_idx, dataloader_idx):
        """Implement a evaluation/prediction step.

        This function defines the evaluation step. The input batch is from a eval dataloader. Here is the persuade code
        for validating a model:

        ```python
        evaluation_output = []
        for dataloader_idx, dataloader in dataloaders:
            for batch_index, batch in dataloader:
                loss_or_data = evaluation_step(batch, batch_idx)
                evaluation_epoch_output.append(loss_or_data)

        score = evaluation_epoch_end(evaluation_epoch_output)
        return score
        ```

        Notes:
            - The evaluation step will be run on all processes.
            - About batch size: If your evaluation data have the same length, you may use a batch size larger than 1 to
            speed up the evaluation. For example, if you have 1000 samples in the evaluation set, and you have a batch
            size of 100, then you will have 10 batches in the evaluation set. However, if your data in the evaluation
            set has a different length, please use a batch size of 1. It still works for distributed evaluation.
            Otherwise, you will get an error.
            - About distributed evaluation: The output of this function will be gathered across all processes. For
            example, if you have 4 processes, and you have a batch size of 1, then you will have 4 outputs from this
            function. The output of this function will be gathered across all processes. The first dimension of the
            result is num_processes multiplied by the first dimension of the input tensors. **Please make sure the
            first dimension of the input tensors is the batch size.** **The last dimension of the output will be padded
            to the length of the longest sample in the evaluation set.** It means that the output will be a tensor with
            the shape of [num_processes * batch_size, max_length]. If you calculate the metric score on the output, you
            should do a truncation to remove the padding. Otherwise, if you are using a metric that sensitive to the
            padding, you will get a wrong metric score. It is not easy to implement this truncation in the
            ``evaluation_epoch_end`` function. We recommend you directly calculate the metric score in the
            evaluation_step function. I guess the Accelerate team will implement a automatic truncation in the future.
            https://github.com/huggingface/accelerate/issues/226

        Args:
            batch: a batch of data.
            batch_idx: the index of the batch.
            dataloader_idx: the index of the dataloader.

        Returns:
            output: the output of the batch. It can be a list of dict, e.g., [{"metric_1": xx, "metric_2": xx, ...},
            ...]
        """
        raise NotImplementedError

    def evaluation_epoch_end(self, outputs, log_to_tensorboard=True):
        """Evaluation epoch end.

        The input `evaluation_epoch_output` will be a list of list. For example, if you have two dataloaders, the
        `evaluation_epoch_output` will be:

        ```python
        evaluation_epoch_output = [
            [dataloader_1_batch_1_output, dataloader_1_batch_2_output, ...],
            [dataloader_2_batch_1_output, dataloader_2_batch_2_output, ...],
            ...,
        ]
        ```

        The output of this function should be a metric score, which will be used to determine whether the current model
        is the best model.

        ```python
        evaluation_output = []
        for dataloader_idx, dataloader in dataloaders:
            for batch_index, batch in dataloader:
                loss_or_data = evaluation_step(batch, batch_idx)
                evaluation_epoch_output.append(loss_or_data)

        score = evaluation_epoch_end(evaluation_epoch_output)
        return score
        ```


        Args:
            evaluation_epoch_output: the output of the evaluation epoch. It is a list of list.

        Returns:
            score: the metric score of the evaluation epoch.
        """
        # We use this variable to store the score for the current epoch
        score = 0.0

        for dl_id, dataloader_outputs in outputs.items():
            metric_dict_list = []
            for i, step_output in enumerate(dataloader_outputs):
                metric_dict_list += step_output

            # Truncate metrics list to match dataset size when using multiple GPUs
            # This is needed since DDP can pad samples to match the number of GPUs
            dl_length = len(self.eval_dataloaders[dl_id].dataset)  # type: ignore

            if len(metric_dict_list) > dl_length:
                logger.info("You are using #GPUs > 1 for evaluation and #samples is not divisible by the #GPUs.")
                logger.info(f"Truncating the redundant samples ({len(metric_dict_list)} -> {dl_length}).")

                metric_dict_list = metric_dict_list[:dl_length]

            # Use pandas to compute the mean of all metrics and save them to a csv file
            df_metrics = pd.DataFrame(metric_dict_list)
            df_metrics_mean = df_metrics.mean(numeric_only=True)
            df_metrics_mean_df = df_metrics_mean.to_frame().T  # Convert mean to a DataFrame

            time_now = self._current_time_now()
            df_metrics.to_csv(
                self.metrics_dir / f"dl_{dl_id}_epoch_{self.state.epochs_trained}_{time_now}.csv", index=False
            )
            df_metrics_mean_df.to_csv(
                self.metrics_dir / f"dl_{dl_id}_epoch_{self.state.epochs_trained}_{time_now}_mean.csv", index=False
            )

            logger.info(f"\n{df_metrics_mean_df.to_markdown()}")

            # We use the `metric_for_best_model` to compute the score.
            if self.in_training:
                try:
                    score += df_metrics_mean[self.args.metric_for_best_model]
                except KeyError:
                    logger.warning(f"Metric '{self.args.metric_for_best_model}' not found in the evaluation metrics.")
                    logger.warning("You won't be able to use this metric to determine the best model.")
                    logger.warning("Please check the return in your `evaluation_step` function.")
                    score += 0.0

                if log_to_tensorboard:
                    for metric, value in df_metrics_mean.items():
                        self.writer.add_scalar(f"metrics_{dl_id}/{metric}", value, self.state.epochs_trained)

        return score
