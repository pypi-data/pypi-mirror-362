import logging
from pathlib import Path
from typing import Union

import librosa
import numpy as np
import onnxruntime as ort
import torch
from pystoi import stoi as stoi_backend

from audiozen.utils import check_same_shape


def preprocessing(est, ref):
    if est.ndim != 1 or ref.ndim != 1:
        est = est.reshape(-1)
        ref = ref.reshape(-1)

    check_same_shape(est, ref)

    if torch.is_tensor(est) or torch.is_tensor(ref):
        est = est.detach().cpu().numpy()
        ref = ref.detach().cpu().numpy()

    return est, ref


def stoi(*, est, ref, sr=16000):
    # We use `*` to force the user to use keyword arguments to make the order clear.
    est, ref = preprocessing(est, ref)
    stoi_val = stoi_backend(ref, est, sr, extended=False)

    return stoi_val


def estoi(*, est, ref, sr=16000):
    # We use `*` to force the user to use keyword arguments to make the order clear.
    est, ref = preprocessing(est, ref)
    stoi_val = stoi_backend(ref, est, sr, extended=True)

    return stoi_val


class STOI:
    def __init__(self, sr=16000) -> None:
        self.sr = sr

    def __call__(self, est, ref):
        stoi_val = stoi(est=est, ref=ref, sr=self.sr)
        return stoi_val


class eSTOI:
    def __init__(self, sr=16000) -> None:
        self.sr = sr

    def __call__(self, est, ref):
        estoi_val = estoi(est=est, ref=ref, sr=self.sr)
        return estoi_val


__all__ = ["STOI", "eSTOI", "stoi", "estoi"]
