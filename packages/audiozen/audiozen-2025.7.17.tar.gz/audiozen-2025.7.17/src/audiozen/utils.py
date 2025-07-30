import gc
import importlib
import logging
import os
import random
import time
from typing import Optional

import numpy as np
import torch
from torch import Tensor

from audiozen.accelerate import broadcast_tensor, get_world_size_and_rank


logger = logging.getLogger(__name__)


def check_same_shape(est: Tensor, ref: Tensor) -> None:
    if est.shape != ref.shape:
        raise RuntimeError(f"Dimension mismatch: {est.shape=} vs {ref.shape=}.")


def avoid_nan_grad(optimizer: torch.optim.Optimizer) -> None:
    for group in optimizer.param_groups:
        for p in group["params"]:
            if p.grad is not None and (torch.isnan(p.grad).any() or torch.isinf(p.grad).any()):
                print("NaN or INF found in optimizer gradient")


def avoid_nan_value(tensor: Tensor) -> Tensor:
    if torch.isnan(tensor).any() or torch.isinf(tensor).any():
        logger.warning(f"NaN or INF found in tensor. Shape: {tensor.shape}.")
        tensor[torch.isnan(tensor)] = 0
        tensor[torch.isinf(tensor)] = 0
    return tensor


class Timer:
    """Count execution time.

    Examples:
        >>> timer = ExecutionTime()  # Start timer
        >>> print(f"Finished in {timer.duration()} seconds.")
    """

    def __init__(self):
        self.start_time = time.perf_counter()

    def duration(self, ndigits=3):
        """Get duration of execution.

        Args:
            ndigits: number of digits to round. Default: 3.
        """
        duration = round(time.perf_counter() - self.start_time, ndigits)
        return duration


def log_header(text: str, header_length=78, block_char="="):
    """Print a pretty header in green with a black background"""

    # Limit the length of the text to fit the header
    max_text_length = header_length - 2
    if len(text) > max_text_length:
        text = text[: max_text_length - 3] + "..."
    content = f" {text} "

    logger.info(block_char * header_length, stacklevel=2)
    # Use center() to automatically pad left and right, aligning the length to header_length
    logger.info(content.center(header_length, block_char), stacklevel=2)
    logger.info(block_char * header_length, stacklevel=2)


def instantiate(path: str, args: Optional[dict] = None, initialize: bool = True):
    """Load module or callable (like function) dynamically based on config string.

    Assume that the config items are as follows:

        [model]
            path = "model.FullSubNetModel"
            [model.args]
            n_frames = 32
            ...

    This function will:
        1. Load the "model" module from python search path.
        2. Load "model.FullSubNetModel" class or callable in the "model" module.
        3. If the "initialize" is set to True, instantiate (or call) class (or callable) with args (in "[model.args]").

    Args:
        path: Target class or callable path.
        args: Named arguments passed to class or callable.
        initialize: whether to initialize with args.

    Returns:
        If initialize is True, return the instantiated class or the return of the call.
        Otherwise, return the found class or callable

    Examples:
        >>> # Use official loss function
        >>> instantiate("torch.nn.CrossEntropyLoss", args={"label_smoothing": 0.2}, initialize=True)
        >>> # Use official optimizer
        >>> instantiate("torch.optim.Adam", args={"lr": 1e-3}, initialize=True)
        >>> # Use custom model in a recipe
        >>> instantiate("fsb.model.FullSubNetModel", args={"n_frames": 32}, initialize=True)
        >>> # Use custom loss function in audiozen
        >>> instantiate("audiozen.loss.CRMLoss", initialize=False)
    """
    # e.g., path = "fsb.model.FullSubNetModel"
    # module_path = "fsb.model"
    # class_or_function_name = "FullSubNetModel"
    splitted_path = path.split(".")

    if len(splitted_path) < 2:
        raise ValueError(f"Invalid path: {path}.")

    module_path = ".".join(splitted_path[:-1])
    class_or_function_name = splitted_path[-1]

    module = importlib.import_module(module_path)
    class_or_function = getattr(module, class_or_function_name)

    if initialize:
        if args:
            return class_or_function(**args)
        else:
            return class_or_function()
    else:
        return class_or_function


def set_random_seed(seed: Optional[int] = None):
    """Set random seed for reproducibility.

    Note:
        This function is used to control the reproducibility of the training process.
    """
    world_size, rank = get_world_size_and_rank()
    max_val = np.iinfo(np.uint32).max - world_size + 1
    min_val = np.iinfo(np.uint32).min

    if seed is None:
        rand_seed = torch.randint(min_val, max_val, (1,))
        seed = broadcast_tensor(rand_seed, 0).item()  # sync seed across ranks

    if seed < min_val or seed > max_val:
        raise ValueError(f"Invalid seed value provided: {seed}. Value must be in the range [{min_val}, {max_val}]")

    if rank == 0:
        logger.info(f"Setting manual seed to local seed + rank: {seed + rank}.")

    random.seed(seed + rank)
    np.random.seed(seed + rank)
    torch.manual_seed(seed + rank)


def cleanup_before_training() -> None:
    """Call gc collect, empty CUDA cache, and reset peak memory stats."""
    gc.collect()
    torch.cuda.empty_cache()
    torch.cuda.reset_peak_memory_stats()


def prepare_dirs(dirs):
    """Prepare directories..

    This function creates the specified directories if they don't exist.

    Args:
        dirs: a list of Path objects.
    """
    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)


def prepare_empty_dir(dirs, resume=False):
    """Prepare empty dirs.

    If resume a experiment, this function only assert that dirs should be exist.
    If does not resume a experiment, this function will set up new dirs.

    Args:
        dirs: a list of Path objects.
        resume: whether to resume a experiment. Default: False.
    """
    for dir_path in dirs:
        if resume:
            if not dir_path.exists():
                logger.warning(f"In resume mode, you must have an old experiment directory {dir_path}.")
        else:
            dir_path.mkdir(parents=True, exist_ok=True)


def expand_path(path):
    return os.path.abspath(os.path.expanduser(path))


def clamp_inf_value(tensor):
    """Clamp inf value to a large number."""
    max_dtype = torch.finfo(tensor.dtype).max
    clamp_value = torch.where(torch.isinf(tensor).any(), max_dtype - 1000, tensor)
    tensor = torch.clamp(tensor, min=-clamp_value, max=clamp_value)
    return tensor
