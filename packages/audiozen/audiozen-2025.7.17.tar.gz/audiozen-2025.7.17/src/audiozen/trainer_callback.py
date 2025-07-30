import logging
from abc import ABC, abstractmethod
from typing import Optional

from audiozen.accelerate import is_rank_zero
from audiozen.trainer import TrainerControl


logger = logging.getLogger(__name__)


class TrainerCallback:
    """Base class for all callbacks.

    Callbacks are objects that can customize the behavior of the training loop in the Trainer that can inspect the
    training loop state (for progress reporting, logging on TensorBoard or other ML platforms…) and do some actions at
    specific points in the training loop (for example, pruning the model).

    Note:
        1. For the most cases, callbacks are **"read only"** pieces of code, apart from the `TrainerControl` object
           they return, they cannot change anything in the training loop. For customizations that require changes in
           the training loop, you should subclass Trainer and override the methods you need.
        2. The trainer instance is stored in `self.trainer`. This is different from the `Trainer` class. Although we
           don't recommend it, you can also use it to change the model, the optimizer, or the learning rate scheduler.
           If you do so, you should notify in the comment that **the callback is modifying the trainer state** to avoid
           confusion.

    Reference:
        HuggingFace Callbacks: https://huggingface.co/docs/transformers/en/main_classes/callback.
    """

    def __init__(self):
        self.trainer = None

    def on_train_begin(self, control: TrainerControl, **kwargs) -> Optional[TrainerControl]:
        """Event called at the beginning of a training step."""
        pass

    def on_training_step_begin(self, control: TrainerControl, **kwargs) -> Optional[TrainerControl]:
        """Event called at the beginning of training."""
        pass

    def on_training_step_before_return_loss_dict(self, control: TrainerControl, **kwargs) -> Optional[TrainerControl]:
        """Event called at the end of training step before returning the loss dict."""
        pass

    def on_evaluation_begin(self, control: TrainerControl, **kwargs) -> Optional[TrainerControl]:
        """Event called at the beginning of the evaluation loop."""
        pass


class StatefulTrainerCallback(TrainerCallback, ABC):
    """An abstract base class for TrainerCallbacks that have a state to be saved and loaded."""

    @abstractmethod
    def state_dict(self) -> dict:
        """Returns the state of the callback as a dictionary."""
        pass

    @abstractmethod
    def load_state_dict(self, state_dict: dict):
        """Loads the callback's state from a dictionary."""
        pass


class CallbackHandler(TrainerCallback):
    """Internal class that just calls the list of callbacks in order."""

    def __init__(self, callbacks: Optional[list[TrainerCallback]] = None, trainer=None):
        super().__init__()

        self.callbacks = []

        if callbacks is not None:
            for cb in callbacks:
                if isinstance(cb, TrainerCallback):
                    # Set the trainer instance for the callback
                    # Why not set the trainer during callback class initialization?
                    # Because the trainer instance is not available when the callback is created.
                    cb.trainer = trainer
                    self.callbacks.append(cb)
                    if is_rank_zero():
                        logger.info(f"Added a callback: {cb.__class__.__name__}")

                else:
                    raise ValueError(f"Callback {cb} must be an instance of `TrainerCallback`.")

        if is_rank_zero():
            logger.info(f"Callback handler initialized with {len(self.callbacks)} callbacks.")

    def call_event(self, event: str, control: TrainerControl, **kwargs):
        """Call a specific event on all callbacks.

        Args:
            event: The event to call.
            **kwargs: Additional keyword arguments to pass to the callback method.

        Example of how this works:
            1. `self.callback_handler.on_train_begin(...)` is called in the trainer.
            2. The `call_event` method is called with the `event` name and `control` object.
            3. For each callback in self.callbacks, if the callback has a method with the name of the event, it is
               called with the control object and additional keyword arguments.
            4. The control object is updated with the result of the callback method.
        """
        for callback in self.callbacks:
            logger.info(f"Calling {event} on {callback.__class__.__name__}")

            # The control passed in is the version after the last callback was processed (or the initial version)
            result = getattr(callback, event)(control, **kwargs)

            # A Callback can skip the return of `control` if it doesn't change it.
            if result is not None:
                control = result

        # return the control object after all callbacks on the **current** event have been called
        return control

    ###################################
    # Shortcut methods
    ###################################
    # Why we need this kind of method?
    # If no this method, we need to call `on_train_begin` manually in the trainer. e.g,
    # self.callback_handler.call_callbacks("on_train_begin")
    # Cause these callback name are very simliar, you may write some typos.
    # So we add this method to call `on_train_begin`.
    def on_train_begin(self, control: TrainerControl, **kwargs):
        return self.call_event("on_train_begin", control, **kwargs)

    def on_training_step_begin(self, control: TrainerControl, **kwargs):
        return self.call_event("on_training_step_begin", control, **kwargs)

    def on_training_step_before_return_loss_dict(self, control: TrainerControl, **kwargs):
        return self.call_event("on_training_step_before_return_loss_dict", control, **kwargs)

    def on_evaluation_begin(self, control: TrainerControl, **kwargs):
        return self.call_event("on_evaluation_begin", control, **kwargs)
