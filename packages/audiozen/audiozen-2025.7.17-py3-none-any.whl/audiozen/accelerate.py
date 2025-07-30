import logging
from typing import Tuple

import torch
import torch.distributed as dist
from torch import Tensor


logger = logging.getLogger(__name__)


def init_accelerator(device: str = "cpu") -> Tuple[int, int]:
    """Setup the accelerator.

    Return the world size and current rank.

    Note:
        * The AudioZen library only supports CPU and NVIDIA GPUs.
        * For CPU, you can set the `device` to `cpu`. Then just perform `python script.py` and it will run on CPU.
        * For GPU, we use `torch.distributed` to run on multiple GPUs. You may set the `device` to `gpu` and run the
        script with `torchrun` command. For example, `torchrun --nproc_per_node=2 script.py` will run the script on 2
        GPUs.
        * You may found the following code snippet is very short and simple, but it's very useful for these two cases.

    Args:
        device: Device. Defaults to `cpu`. Can be `cpu` or `gpu`.
    """
    world_size, rank = 1, 0

    if device == "gpu":
        assert torch.cuda.is_available(), "CUDA device requested but not available."
        # Initialize the default distributed process group
        dist.init_process_group(backend="nccl")

        # Some PyTorch APIs will use the `torch.cuda.current_device()` to get the current device, e.g., gather(). So,
        # we need to set the current device to the rank of the current process. Otherwise, those APIs will be failed,
        # e.g., gather() will hang if the current device is not set.
        torch.cuda.set_device(dist.get_rank())

        world_size, rank = dist.get_world_size(), dist.get_rank()
    elif device == "cpu":
        pass
    else:
        raise ValueError(f"Invalid device: {device}. Please choose 'cpu' or 'gpu'.")

    # We don't use logging here because the logger may not be initialized yet.
    print(f"Accelerator initialized with device `{device}`. World size: {world_size}, Rank: {rank}")

    return world_size, rank


def get_rank() -> int:
    """Function that gets the rank number of the current process in the default process group.

    Returns:
        int: rank
    """
    if dist.is_available() and dist.is_initialized():
        return dist.get_rank()
    else:
        return 0


def get_world_size_and_rank() -> Tuple[int, int]:
    """Function that gets the current world size (aka total number of ranks) and rank number of the current process in
    the default process group.

    Return the world size and rank of the current process.
    """
    if dist.is_available() and dist.is_initialized():
        return dist.get_world_size(), dist.get_rank()
    else:
        return 1, 0


def is_rank_zero() -> bool:
    """Check if the current process is rank 0.

    Returns:
        bool: True if rank is 0, False otherwise.
    """
    return get_rank() == 0


def broadcast_tensor(tensor: Tensor, src: int = 0) -> Tensor:
    """Broadcast a tensor to all other processes.

    Args:
        tensor: The tensor to broadcast.
        src: Source rank. Defaults to 0.
    """
    if dist.is_available() and dist.is_initialized():
        # Broadcasts the tensor to all other processes in the process group.
        # Now tensor values are the same across all processes.
        dist.broadcast(tensor, src=src, async_op=False)
        return tensor
    else:
        logger.warning("Distributed environment not initialized. No broadcast will be performed.")
        return tensor


def wait_for_everyone():
    """Will stop the execution of the current process until every other process has reached that point (so this does
    nothing when the script is only run in one process).

    Note:
        After pytorch 2.5, we need to add a device_ids argument to the barrier function.

    Useful to do before saving a model. It only works if the accelerator is set to "gpu". If the accelerator is set to
    "cpu", it will do nothing.
    """
    if dist.is_available() and dist.is_initialized():
        dist.barrier(device_ids=[get_rank()])
    else:
        logger.warning("Distributed environment not initialized. No barrier will be performed.")


def gather_object(object, dst=0):
    """Gather a single object from all processes and returns it to the destination process.

    Args:
        object: The object to gather.
        dst: Destination rank. Defaults to 0.
    """
    if dist.is_available() and dist.is_initialized():
        # `object_gather_list` means a placeholder for the collected step_output from all processes.
        # `len(object_gather_list)` >= `world_size`, the extra elements will stay as `None`.
        # `len(object_gather_list)` < `world_size`, the program will raise an error.
        # The rank 0 process will gather the step_output from all processes. Other processes will not gather the
        # step_output and keep all `None`.
        output = [None for _ in range(dist.get_world_size())]
        dist.gather_object(object, output if is_rank_zero() else None, dst=dst)
        # `gather_object` returns a list of lists, so we need to flatten it
        if is_rank_zero():
            return [x for y in output for x in y]  # type: ignore
        else:
            return None
    else:
        raise RuntimeError("Distributed environment not initialized. No gather will be performed.")
