from dataclasses import dataclass
from pathlib import Path

import librosa
from simple_parsing import Serializable
from torch.utils.data import Dataset

from audiozen.acoustics.io import extract_segment


@dataclass
class NaiveNoisyCleanDatasetArgs(Serializable):
    """Configuration arguments for the NaivePairedNoisyCleanDataset class."""

    # Root directory containing audio files
    dataset_root_dir: str = "datasets/VoiceBank-Demand"
    # Audio sample length in seconds. If <= 0, loads complete files.
    audio_sample_len_in_sec: int = 4
    # Offset and limit for dataset
    offset: int = -1
    limit: int = -1
    sr: int = 16000
    # Subdirectory names for noisy and clean audio files
    noisy_subdir: str = "noisy"
    clean_subdir: str = "clean"


class NaivePairedNoisyCleanDataset(Dataset):
    """A dataset class for loading paired noisy and clean audio files."""

    def __init__(self, args: NaiveNoisyCleanDatasetArgs):
        """Initialize the dataset with the given arguments.

        Args:
            args: Configuration arguments for the dataset.

        """
        super().__init__()
        self.args = args

        dataset_root_dir = Path(args.dataset_root_dir).expanduser().resolve()

        self.noisy_root_dir = dataset_root_dir / args.noisy_subdir
        self.clean_root_dir = dataset_root_dir / args.clean_subdir

        if not self.noisy_root_dir.exists():
            raise FileNotFoundError(f"Directory not found: {self.noisy_root_dir}")

        if not self.clean_root_dir.exists():
            raise FileNotFoundError(f"Directory not found: {self.clean_root_dir}")

        self.noisy_audio_fpath_list = librosa.util.find_files(self.noisy_root_dir)
        self.clean_audio_fpath_list = librosa.util.find_files(self.clean_root_dir)

        assert len(self.noisy_audio_fpath_list) == len(self.clean_audio_fpath_list), (
            f"Number of noisy and clean audio files must be equal. "
            f"Found {len(self.noisy_audio_fpath_list)} noisy files and "
            f"{len(self.clean_audio_fpath_list)} clean files."
        )

        if args.offset > 0:
            self.noisy_audio_fpath_list = self.noisy_audio_fpath_list[args.offset :]
            self.clean_audio_fpath_list = self.clean_audio_fpath_list[args.offset :]

        if args.limit > 0:
            step = max(len(self.noisy_audio_fpath_list) // args.limit, 1)
            self.noisy_audio_fpath_list = self.noisy_audio_fpath_list[::step]
            self.clean_audio_fpath_list = self.clean_audio_fpath_list[::step]

        if args.audio_sample_len_in_sec > 0:
            self.audio_sample_len_in_samples = int(args.audio_sample_len_in_sec * args.sr)

    def __len__(self):
        return len(self.noisy_audio_fpath_list)

    def __getitem__(self, idx):
        noisy_fpath = self.noisy_audio_fpath_list[idx]
        clean_fpath = self.clean_audio_fpath_list[idx]
        stem = Path(noisy_fpath).stem  # The final path component, without its suffix

        noisy_y, _ = librosa.load(noisy_fpath, sr=self.args.sr)
        clean_y, _ = librosa.load(clean_fpath, sr=self.args.sr)

        if self.args.audio_sample_len_in_sec > 0:
            noisy_y, start_idx = extract_segment(noisy_y, self.audio_sample_len_in_samples)
            clean_y, _ = extract_segment(clean_y, self.audio_sample_len_in_samples, start_idx=start_idx)

        return noisy_y, clean_y, noisy_fpath, clean_fpath
