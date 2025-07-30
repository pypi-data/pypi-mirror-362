import logging
from pathlib import Path
from typing import Any, Optional, Tuple, Union

import librosa
import numpy as np
import soundfile as sf
from numpy import ndarray


logger = logging.getLogger(__name__)


def load_audio(
    path: Union[Path, str],
    *,
    duration: Optional[float] = None,
    sr: Optional[int] = None,
    **kwargs: Any,
) -> Tuple[np.ndarray, int]:
    """Load the audio using soundfile and resample if necessary.

    Compared to sf.read, this function supports:
    - loading the random segment of a audio when duration is specified.
    - resampling the audio when sr is specified.

    Args:
        path: Path to the audio file.
        duration: Duration of the audio segment in seconds. If None, the whole audio is loaded.
        sr: Sampling rate of the audio. If None, the original sampling rate is used.
        **kwargs: Additional keyword arguments for `np.pad`.

    Returns:
        A tuple of the audio signal and the sampling rate.

    Examples:
        >>> load_audio("test.wav", duration=2.0, sr=16000)
    """
    path = str(path)

    with sf.SoundFile(path) as sf_desc:
        orig_sr = sf_desc.samplerate

        if duration is not None:
            frame_orig_duration = sf_desc.frames
            frame_duration = int(duration * orig_sr)

            if frame_duration < frame_orig_duration:
                # Randomly select a segment
                offset = np.random.randint(frame_orig_duration - frame_duration)
                sf_desc.seek(offset)
                y = sf_desc.read(frames=frame_duration, dtype="float32", always_2d=True).T
            else:
                y = sf_desc.read(dtype="float32", always_2d=True).T  # [C, T]
                if frame_duration > frame_orig_duration:
                    y = np.pad(y, pad_width=((0, 0), (0, frame_duration - frame_orig_duration)), **kwargs)
        else:
            y = sf_desc.read(dtype="float32", always_2d=True).T

    if y.shape[0] == 1:
        y = y.flatten()

    if sr is not None and sr != orig_sr:
        y = librosa.resample(y, orig_sr=orig_sr, target_sr=sr)
        orig_sr = sr

    return y, orig_sr


def extract_segment(data: ndarray, segment_length: int, *, start_idx: int = -1) -> Tuple[ndarray, int]:
    """Sample a segment from the N-dimensional data with the last dimension as the time dimension.

    Args:
        data: Any dimensional data. The last dimension is the time dimension.
        segment_length: The length of the segment to be sampled.
        start_idx: The start index of the segment to be sampled. If less than 0, a random index is generated.
        return_start_idx: Whether to return the start index along with the data segment.

    Returns:
        The sampled data segment and the start index.

    Raises:
        ValueError: If segment_length is negative.
    """
    segment_length = int(segment_length)

    if segment_length < 0:
        raise ValueError("`segment_length` must be non-negative")

    data_len = data.shape[-1]
    ndim = data.ndim

    if data_len > segment_length:
        if start_idx >= 0:
            end_idx = start_idx + segment_length
        else:
            start_idx = np.random.randint(data_len - segment_length)
            end_idx = start_idx + segment_length
        data = data[..., start_idx:end_idx]
    elif data_len < segment_length:
        padding = segment_length - data_len
        pad_width = [(0, 0)] * (ndim - 1) + [(0, padding)]
        data = np.pad(data, pad_width, "constant")
        start_idx = 0

    return data, start_idx


def collect_audio_file_paths(
    *,
    directory: Optional[Path] = None,
    directory_list: Optional[list[str]] = None,
    scp_file: Optional[str] = None,
    scp_file_list: Optional[list[str]] = None,
    file_extension: Optional[str] = "wav",
    limit: int = 0,
    random_shuffle: bool = False,
) -> list[str]:
    """Find files in the specified directory, directory list, scp file (s), or a combination of them.

    Args:
        directory: A single directory to search for audio files.
        directory_list: A list of directories to search for audio files.
        scp_file: A file containing a list of audio file paths, one per line.
        scp_file_list: A list of scp file paths, each containing a list of audio file paths.
        file_extension: The extension of audio files to search for (default: "wav").
        limit: Maximum number of files to return (0 means no limit).
        random_shuffle: Whether to randomly shuffle the resulting file list.

    Returns:
        A list of audio file paths.
    """
    audio_paths = []

    if directory is not None:
        audio_paths += librosa.util.find_files(directory, ext=file_extension)

    if directory_list is not None:
        for dir_path in directory_list:
            audio_paths += librosa.util.find_files(dir_path, ext=file_extension)

    if scp_file is not None:
        with open(scp_file, "r") as f:
            audio_paths += [line.strip() for line in f if line.strip()]

    if scp_file_list is not None:
        for scp_path in scp_file_list:
            with open(scp_path, "r") as f:
                audio_paths += [line.strip() for line in f if line.strip()]

    # in-place shuffle the list
    if random_shuffle:
        np.random.shuffle(audio_paths)

    if limit > 0:
        audio_paths = audio_paths[:limit]

    return audio_paths
