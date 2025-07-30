from dataclasses import dataclass

from simple_parsing import Serializable


@dataclass
class ModelArgs(Serializable):
    sr: int = 44100
    n_fft: int = 2048
    win_length: int = 2048
    hop_length: int = 512

    enc_dim: int = 1025
    feat_dim: int = 128
    num_channels: int = 1
    num_layer: int = 1
    num_repeat: int = 6
    dropout: float = 0.0
