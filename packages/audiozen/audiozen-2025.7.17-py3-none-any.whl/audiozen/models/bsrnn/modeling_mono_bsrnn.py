from dataclasses import dataclass
from functools import partial
from typing import List, Literal, Optional, Tuple, Union

import numpy as np
import torch
import torch.nn as nn
from einops import rearrange
from torch import Tensor


@dataclass
class ModelArgs:
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


def mag_phase(complex_valued_tensor: Tensor) -> tuple[Tensor, Tensor]:
    """Get magnitude and phase of a complex-valued tensor.

    Args:
        complex_valued_tensor: complex-valued tensor.

    Returns:
        magnitude and phase spectrogram.
    """
    mag, phase = torch.abs(complex_valued_tensor), torch.angle(complex_valued_tensor)
    return mag, phase


def real_imag(complex_valued_tensor: Tensor) -> tuple[Tensor, Tensor]:
    """Get real and imag part of a complex-valued tensor.

    Args:
        complex_valued_tensor: complex-valued tensor.

    Returns:
        real and imag spectrogram.
    """
    return complex_valued_tensor.real, complex_valued_tensor.imag


def istft(
    feature: Union[Tensor, Tuple[Tensor, Tensor], List[Tensor]],
    n_fft: int,
    hop_length: int,
    win_length: int,
    window: Optional[str] = "hann",
    length: Optional[int] = None,
    input_type: Literal["mag_phase", "real_imag", "complex", "complex_view_as_real"] = "mag_phase",
) -> Tensor:
    if input_type == "real_imag":
        if isinstance(feature, (tuple, list)) and len(feature) == 2:
            real, imag = feature
            complex_valued_features = torch.complex(real=real, imag=imag)
        else:
            raise ValueError("For 'real_imag', provide a tuple or list with two elements: (real, imag).")

    elif input_type == "complex":
        if isinstance(feature, Tensor) and torch.is_complex(feature):
            complex_valued_features = feature
        else:
            raise ValueError("For 'complex', provide a complex-valued tensor.")

    elif input_type == "complex_view_as_real":
        assert isinstance(feature, Tensor), "For 'complex_view_as_real', provide a complex-valued tensor."
        if feature.ndim == 4 and feature.shape[1] == 2:
            real, imag = feature[:, 0, ...], feature[:, 1, ...]
            complex_valued_features = torch.complex(real=real, imag=imag)
        else:
            raise ValueError("For 'complex_view_as_real', provide a 4D tensor with shape [B, 2, F, T].")

    elif input_type == "mag_phase":
        if isinstance(feature, (tuple, list)) and len(feature) == 2:
            mag, phase = feature
            complex_valued_features = torch.polar(mag, phase)
        else:
            raise ValueError("For 'mag_phase', provide a tuple or list with two elements: (magnitude, phase).")

    else:
        raise ValueError(f"Unsupported input_type: {input_type}")

    if window is not None:
        window_func = getattr(torch, f"{window}_window", None)
        if window_func is None:
            raise ValueError(f"Unsupported window type: {window}")
        window_initialized = window_func(win_length, device=complex_valued_features.device)
    else:
        window_initialized = torch.ones(win_length, device=complex_valued_features.device)

    return torch.istft(
        input=complex_valued_features,
        n_fft=n_fft,
        hop_length=hop_length,
        win_length=win_length,
        window=window_initialized,
        length=length,
    )


def stft(
    y,
    n_fft,
    hop_length,
    win_length,
    window="hann",
    output_type: Literal["mag_phase", "real_imag", "complex"] | None = None,
    **kwargs,
) -> tuple[Tensor, ...] | Tensor:
    """Wrapper of the official ``torch.stft`` for single-channel and multichannel signals.

    Args:
        y (`torch.Tensor` of shape `(batch_size, num_channels, num_samples) or `(batch_size, num_samples)`):
            single-/multichannel signals.
        n_fft: num of FFT.
        hop_length: hop length.
        win_length: hanning window size.
        output_type: "mag_phase", "real_imag", "complex", or None. Defaults to None.
        kwargs: other arguments for ``torch.stft``.

    Returns:
        If the input is single-channel, return the spectrogram with shape of [B, F, T], otherwise [B, C, F, T].
        If output_type is "mag_phase", return a list of magnitude and phase spectrogram.
        If output_type is "real_imag", return a list of real and imag spectrogram.
        If output_type is None, return a list of magnitude, phase, real, and imag spectrogram.
    """
    # logger.warning("This function is deprecated. Please use `stft_v2` instead.")

    # Support [B, T] and [B, C, T]
    if y.ndim not in [2, 3]:
        raise ValueError(f"Only support single-/multi-channel signals. Received {y.ndim=}.")

    is_multi_channel = y.ndim == 3

    batch_size, *_, num_samples = y.shape

    # Compatible with multi-channel signals
    if is_multi_channel:
        y = y.reshape(-1, num_samples)

    if window is not None:
        window_func = getattr(torch, f"{window}_window")
        window = window_func(win_length, device=y.device)
    else:
        window = torch.ones(n_fft, device=y.device)

    complex_stft = torch.stft(
        input=y,
        n_fft=n_fft,
        hop_length=hop_length,
        win_length=win_length,
        window=window,
        return_complex=True,
        **kwargs,
    )

    # Reshape back to original if the input is multi-channel
    if is_multi_channel:
        complex_stft = complex_stft.reshape(batch_size, -1, *complex_stft.shape[-2:])

    if output_type == "mag_phase":
        return mag_phase(complex_stft)
    elif output_type == "real_imag":
        return real_imag(complex_stft)
    elif output_type == "complex":
        return complex_stft
    else:
        mag, phase = mag_phase(complex_stft)
        return mag, phase, complex_stft.real, complex_stft.imag


class ResRNN(nn.Module):
    def __init__(self, input_size, hidden_size, bidirectional=True, residual=True):
        super(ResRNN, self).__init__()

        self.input_size = input_size
        self.hidden_size = hidden_size
        self.residual = residual
        self.eps = 1e-6

        self.norm = nn.GroupNorm(1, input_size, self.eps)
        self.rnn = nn.LSTM(input_size, hidden_size, 1, batch_first=True, bidirectional=bidirectional)

        # linear projection layer
        self.proj = nn.Linear(hidden_size * (int(bidirectional) + 1), input_size)

    def forward(self, input):
        # input shape: batch, dim, seq

        rnn_output, _ = self.rnn(self.norm(input).transpose(1, 2).contiguous())
        rnn_output = self.proj(rnn_output.contiguous().view(-1, rnn_output.shape[2])).view(
            input.shape[0], input.shape[2], input.shape[1]
        )
        rnn_output = rnn_output.transpose(1, 2).contiguous()

        if self.residual:
            return input + rnn_output
        else:
            return rnn_output


class BSNet(nn.Module):
    def __init__(self, in_channel, num_bands=7, num_layer=1):
        super(BSNet, self).__init__()

        self.num_bands = num_bands
        self.feat_dim = in_channel // num_bands

        self.band_rnn = []
        for _ in range(num_layer):
            self.band_rnn.append(ResRNN(self.feat_dim, self.feat_dim * 2, bidirectional=True))
        self.band_rnn = nn.Sequential(*self.band_rnn)
        self.band_comm = ResRNN(self.feat_dim, self.feat_dim * 2, bidirectional=True)

    def forward(self, input):
        input, active_nband, bsnet_layer = (input[0], input[1], input[2])

        # input shape: B, nband*N, T
        B, N, T = input.shape
        # Fuse the tsvad_embedding and subband feature

        input = input.view(B * self.num_bands, self.feat_dim, -1)

        if active_nband is None:
            band_output = self.band_rnn(input).view(B, self.num_bands, -1, T)  # type: ignore
            # band comm
            band_output = band_output.permute(0, 3, 2, 1).contiguous().view(B * T, -1, self.num_bands)
            output = self.band_comm(band_output).view(B, T, -1, self.num_bands).permute(0, 3, 2, 1).contiguous()
            return output.view(B, N, T)
        else:
            band_output = self.band_rnn(input).view(B, active_nband, -1, T)  # type: ignore

            # band comm
            band_output = band_output.permute(0, 3, 2, 1).contiguous().view(B * T, -1, active_nband)
            output = self.band_comm(band_output).view(B, T, -1, active_nband).permute(0, 3, 2, 1).contiguous()

            return [output.view(B, N, T), active_nband, bsnet_layer + 1]


class Model(nn.Module):
    def __init__(self, args: ModelArgs):
        super(Model, self).__init__()
        self.args = args

        # 0-1k (100 hop), 1k-4k (250 hop), 4k-8k (500 hop), 8k-16k (1k hop), 16k-20k (2k hop), 20k-inf
        bandwidth_100 = int(np.floor(100 / (args.sr / 2.0) * args.enc_dim))
        bandwidth_250 = int(np.floor(250 / (args.sr / 2.0) * args.enc_dim))
        bandwidth_500 = int(np.floor(500 / (args.sr / 2.0) * args.enc_dim))
        bandwidth_1k = int(np.floor(1000 / (args.sr / 2.0) * args.enc_dim))
        # bandwidth_2k = int(np.floor(2000 / (args.sr / 2.0) * args.enc_dim))
        self.band_width = [bandwidth_100] * 10
        self.band_width += [bandwidth_250] * 12
        self.band_width += [bandwidth_500] * 8
        self.band_width += [bandwidth_1k] * 8
        # self.band_width += [bandwidth_2k] * 2
        self.band_width.append(int(args.enc_dim - np.sum(self.band_width)))
        self.n_band = len(self.band_width)
        print(self.band_width)

        self.eps = 1e-6
        ri_dim = 2

        self.BN = nn.ModuleList([])
        for i in range(self.n_band):
            self.BN.append(
                nn.Sequential(
                    nn.GroupNorm(1, self.band_width[i] * ri_dim * args.num_channels, self.eps),
                    nn.Conv1d(self.band_width[i] * ri_dim * args.num_channels, args.feat_dim, 1),
                )
            )

        self.separator = []
        for i in range(args.num_repeat):
            self.separator.append(BSNet(self.n_band * args.feat_dim, self.n_band, args.num_layer))
        self.separator = nn.Sequential(*self.separator)

        self.mask = nn.ModuleList([])
        for i in range(self.n_band):
            self.mask.append(
                nn.Sequential(
                    nn.GroupNorm(1, args.feat_dim, self.eps),
                    nn.Conv1d(args.feat_dim, args.feat_dim * 2, 1),
                    nn.Tanh(),
                    nn.Conv1d(args.feat_dim * 2, args.feat_dim * 2, 1),
                    nn.Tanh(),
                    nn.Conv1d(args.feat_dim * 2, self.band_width[i] * 4 * 2, 1),
                )
            )

        self.args = args
        self.stft = partial(stft, n_fft=args.n_fft, hop_length=args.hop_length, win_length=args.win_length)
        self.istft = partial(istft, n_fft=args.n_fft, hop_length=args.hop_length, win_length=args.win_length)

    def forward(self, noisy_y):
        # noisy_y: [B, C, T] or [B, T]
        # enh_y: [B, T]
        if noisy_y.dim() == 2:
            noisy_y = noisy_y.unsqueeze(1)

        nsample = noisy_y.size(-1)
        mag_mix, phase_mix, real_mix, imag_mix = self.stft(noisy_y)  # [B=2, C=1, F=1025, T=87]
        batch_size, num_channels, n_frame = noisy_y.shape

        # Sub-band-wise RNN
        spec_RI = torch.cat([real_mix, imag_mix], 1)  # B, C * ri, F, T
        spec = torch.complex(real_mix, imag_mix)  # B, C, F, T
        subband_spec_RI = []
        subband_spec_complex = []
        band_idx = 0
        for i in range(len(self.band_width)):
            # B, C * ri, Fs, T
            subband_spec_ri_i = spec_RI[:, :, band_idx : band_idx + self.band_width[i]].contiguous()
            # B, Fs, T
            subband_spec_complex_i = spec[:, 0, band_idx : band_idx + self.band_width[i]].contiguous()
            subband_spec_RI.append(subband_spec_ri_i)
            subband_spec_complex.append(subband_spec_complex_i)
            band_idx += self.band_width[i]

        subband_feat = []
        for i in range(len(self.band_width)):
            subband_spec_RI_i = rearrange(subband_spec_RI[i], "b c fs t -> b (c fs) t")  # [B, ri * C * Fs, T]
            subband_feat.append(self.BN[i](subband_spec_RI_i))  # [B, e, T]
        subband_feat = torch.stack(subband_feat, 1)  # [B, n_band, e, T],

        # separator
        # [B, n_band*N, T]
        sep_output = self.separator([rearrange(subband_feat, "b n e t -> b (n e) t"), self.n_band, 0])  # type: ignore

        if isinstance(sep_output, list):
            sep_output = sep_output[0]
        sep_output = sep_output.view(batch_size, self.n_band, self.args.feat_dim, -1)

        spk_1_sep_subband_spec = []
        spk_2_sep_subband_spec = []
        for i in range(len(self.band_width)):
            this_output = self.mask[i](sep_output[:, i]).view(batch_size, 2, 2, 2, self.band_width[i], -1)

            this_mask = this_output[:, 0] * torch.sigmoid(this_output[:, 1])  # B*nch, 2, 2, BW, T
            this_mask_real = this_mask[:, 0]  # B*nch, BW, T
            this_mask_imag = this_mask[:, 1]  # B*nch, BW, T

            spk_1_this_mask_real, spk_2_this_mask_real = this_mask_real[:, 0], this_mask_real[:, 1]
            spk_1_this_mask_imag, spk_2_this_mask_imag = this_mask_imag[:, 0], this_mask_imag[:, 1]

            spk_1_est_spec_real = (
                subband_spec_complex[i].real * spk_1_this_mask_real
                - subband_spec_complex[i].imag * spk_1_this_mask_imag
            )  # B*nch, BW, T
            spk_1_est_spec_imag = (
                subband_spec_complex[i].real * spk_1_this_mask_imag
                + subband_spec_complex[i].imag * spk_1_this_mask_real
            )  # B*nch, BW, T

            spk_2_est_spec_real = (
                subband_spec_complex[i].real * spk_2_this_mask_real
                - subband_spec_complex[i].imag * spk_2_this_mask_imag
            )
            spk_2_est_spec_imag = (
                subband_spec_complex[i].real * spk_2_this_mask_imag
                + subband_spec_complex[i].imag * spk_2_this_mask_real
            )

            spk_1_sep_subband_spec.append(torch.complex(spk_1_est_spec_real, spk_1_est_spec_imag))
            spk_2_sep_subband_spec.append(torch.complex(spk_2_est_spec_real, spk_2_est_spec_imag))

        spk_1_est_spec = torch.cat(spk_1_sep_subband_spec, 1)  # B*nch, F, T
        if spec.shape[1] > spk_1_est_spec.shape[1]:
            spk_1_est_spec = torch.cat([spk_1_est_spec, spec[:, spk_1_est_spec.shape[1] :, :]], 1)

        spk_2_est_spec = torch.cat(spk_2_sep_subband_spec, 1)
        if spec.shape[1] > spk_2_est_spec.shape[1]:
            spk_2_est_spec = torch.cat([spk_2_est_spec, spec[:, spk_2_est_spec.shape[1] :, :]], 1)

        output_1 = self.istft(spk_1_est_spec, length=nsample, input_type="complex")
        output_2 = self.istft(spk_2_est_spec, length=nsample, input_type="complex")

        output = torch.stack([output_1, output_2], dim=1)

        return output


if __name__ == "__main__":
    batch_size = 2
    num_channels = 1  # 单通道输入信号
    num_samples = 44100  # 1s 采样点数，采样率 44100
    mixture = torch.rand(batch_size, num_channels, num_samples)
    args = ModelArgs()
    model = Model(args)
    output = model(mixture)
    print(output.shape)

    # output: torch.Size([2, 2, 44100])
    # 2: batch_size
    # 2: num_sources
    # 44100: num_samples
