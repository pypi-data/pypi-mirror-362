from dataclasses import dataclass
from pathlib import Path

import librosa
from simple_parsing import Serializable
from torch.utils.data import Dataset


@dataclass
class NaiveNoisyDatasetArgs(Serializable):
    """Configuration arguments for the NaivePairedNoisyCleanDataset class."""

    # Root directory containing audio files
    root_dir: str = "datasets/VoiceBank-Demand"
    offset: int = -1
    limit: int = -1
    sr: int = 16000


class NaiveNoisyDataset(Dataset):
    """A dataset class for loading paired noisy and clean audio files."""

    def __init__(self, args: NaiveNoisyDatasetArgs):
        """Initialize the dataset with the given arguments.

        Args:
            args: Configuration arguments for the dataset.

        """
        super().__init__()
        self.args = args

        self.noisy_root_dir = Path(args.root_dir).expanduser().resolve()

        if not self.noisy_root_dir.exists():
            raise FileNotFoundError(f"Directory not found: {self.noisy_root_dir}")

        self.noisy_audio_fpath_list = librosa.util.find_files(self.noisy_root_dir)

        if args.offset > 0:
            self.noisy_audio_fpath_list = self.noisy_audio_fpath_list[args.offset :]

        if args.limit > 0:
            step = max(len(self.noisy_audio_fpath_list) // args.limit, 1)
            self.noisy_audio_fpath_list = self.noisy_audio_fpath_list[::step]

    def __len__(self):
        return len(self.noisy_audio_fpath_list)

    def __getitem__(self, idx):
        noisy_fpath = self.noisy_audio_fpath_list[idx]

        noisy_y, _ = librosa.load(noisy_fpath, sr=self.args.sr)

        enhanced_fpath = noisy_fpath.replace("noisy", "enhanced")

        return noisy_y, noisy_y, noisy_fpath, noisy_fpath
