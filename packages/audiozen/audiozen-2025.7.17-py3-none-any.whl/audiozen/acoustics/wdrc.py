import math

import fmot
import torch
import torch.nn as nn
from fmot.nn import Sequencer
from fmot.nn.signal_processing import InverseMelFilterBank, Magnitude, MelFilterBank


class _AREMA(Sequencer):
    def __init__(self, features: int, dim: int, attack_time: float, release_time: float, delta_t: float):
        """Sequencer implementation of Attack-Release Exponential Moving Average (AREMA).

        AREMA is used for envelope smoothing to achieve more stable estimates of volume/power/amplitude
        by applying different smoothing coefficients for rising (attack) and falling (release) signal levels.

        Args:
            features: Number of input features.
            dim: Dimension to apply exponential moving average to. Should be the temporal/sequential dimension.
            attack_time: The attack time in seconds (time constant for rising signal levels).
            release_time: The release time in seconds (time constant for falling signal levels).
            delta_t: Time interval between frames (hop size in seconds).
        """
        super().__init__(state_shapes=[[features]], batch_dim=0, seq_dim=dim)
        self.attack_time = attack_time
        self.release_time = release_time

        self.delta_t = delta_t

        # Convert time constants to smoothing coefficients using exponential decay formula
        self.attack_coeff = 1.0 - math.exp(-1.0 * self.delta_t / (self.attack_time))
        self.release_coeff = 1.0 - math.exp(-1.0 * self.delta_t / (self.release_time))

        self.gt0 = fmot.nn.Gt0()

    @torch.jit.export
    def step(self, x_t: torch.Tensor, state: list[torch.Tensor]) -> tuple[torch.Tensor, list[torch.Tensor]]:
        """Computes one step of AREMA processing for the input tensor.

        Args:
            x_t: Current input frame tensor.
            state: List containing the previous frame's output as state[0].

        Returns:
            tuple: A tuple containing (current_output, [current_output_as_next_state]).
        """
        (y_prev,) = state

        # Calculate the difference between current input and previous output
        diff = x_t - y_prev

        # Select attack or release coefficient based on signal direction
        # Use attack coefficient when signal is rising (diff > 0)
        # Use release coefficient when signal is falling (diff <= 0)
        diff_mask = self.gt0(diff)
        alpha = diff_mask * self.attack_coeff + (1 - diff_mask) * self.release_coeff

        # Apply exponential moving average with selected coefficient
        y = alpha * x_t + (1 - alpha) * y_prev

        return y, [y]


class AREMA(nn.Module):
    def __init__(self, features: int, dim: int, attack_time: float, release_time: float, delta_t: float) -> None:
        super().__init__()
        self.arema = _AREMA(features, dim, attack_time, release_time, delta_t)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x, __ = self.arema(x)
        return x


class Limiter(nn.Module):
    def __init__(self, threshold, knee_width: float = 10, min_knee_width=1):
        """Limiter module that prevents signal levels from exceeding a specified threshold.

        The limiter operates in three regions:
        1. Pass-through region (below threshold - knee_width/2): No limiting
        2. Knee region (±knee_width/2 around threshold): Smooth transition into limiting
        3. Limiting region (above threshold + knee_width/2): Hard limiting to threshold

        Args:
            threshold: Maximum allowed signal level in decibels (T).
            knee_width: Width of the transition region in decibels (W). Controls smoothness.
            min_knee_width: Minimum allowed knee width in decibels. Prevents too sharp transitions.
        """
        super().__init__()
        self.threshold = float(threshold)
        self.knee_width = float(knee_width)
        self.gt0 = fmot.nn.Gt0()

        # Pre-compute constants for efficient processing
        self.const_one = self.threshold - self.knee_width / 2  # Start of knee region
        self.const_two = self.knee_width * 2  # Full knee width for normalization

    def forward(self, xG):
        """Apply limiting to input levels.

        Args:
            xG: Input levels in decibels.

        Returns:
            torch.Tensor: Gain values in decibels to be applied to input.
        """
        # Process limiting region (xG > T + W/2)
        limiter_region_mask = self.gt0(2 * (xG - self.threshold) - self.knee_width)

        # Hard limit to threshold in limiting region
        yG = self.threshold * limiter_region_mask + xG * (1 - limiter_region_mask)

        # Process knee region (|xG - T| <= W/2)
        transition_region_mask = self.gt0(self.knee_width - 2 * torch.abs(xG - self.threshold))

        # Apply quadratic curve in knee region for smooth transition to limiting
        yG = (xG - (xG - self.const_one) ** 2 / (self.const_two)) * transition_region_mask + yG * (
            1 - transition_region_mask
        )

        # Calculate required gain to achieve limited output levels
        G = yG - xG
        return G


class DynamicRangeCompressor(nn.Module):
    def __init__(
        self,
        thresholds: list[float] | torch.Tensor,
        ratios: list[float] | torch.Tensor,
        low_level_gains: list[float] | torch.Tensor,
        knee_width: float = 10,
        min_knee_width: float = 2,
    ) -> None:
        """Dynamic Range Compressor with soft knee characteristics.

        This compressor implements three regions of operation:
        1. Linear region (below threshold - knee_width/2): No compression
        2. Knee region (±knee_width/2 around threshold): Smooth transition into compression
        3. Compression region (above threshold + knee_width/2): Full compression at specified ratio

        Notes:
            The threshold determines when compression begins. The knee_width creates a smooth
            transition into compression around the threshold, preventing abrupt gain changes
            that could cause audible artifacts. The compression ratio determines how much the
            signal is attenuated above the threshold.

        Args:
            threshold: The decibel value at which compression starts (T).
            knee_width: Width of the knee region in decibels (W). Determines the smoothness of transition.
            ratio: The compression ratio (R). For every R dB increase in input, output increases by 1 dB.
            min_knee_width: Minimum allowed knee width in decibels. Defaults to 1.
            low_level_gain: Gain applied to low-level signals (under threshold) in decibels.
        """
        super().__init__()
        self.knee_width = float(knee_width)
        self.min_knee_width = float(min_knee_width)

        # Ensure knee_width is not less than min_knee_width
        if self.knee_width < self.min_knee_width:
            self.knee_width = self.min_knee_width

        assert len(thresholds) == len(ratios) == len(low_level_gains), (
            "Thresholds, ratios, and low level gains must have the same length."
        )

        self.thresholds = torch.tensor(thresholds, dtype=torch.float32)
        self.ratios = torch.tensor(ratios, dtype=torch.float32)
        self.low_level_gains = torch.tensor(low_level_gains, dtype=torch.float32)

        # knee 区间边界
        self.x1 = self.thresholds - self.knee_width / 2.0
        self.x2 = self.thresholds + self.knee_width / 2.0

        self.y1 = self.x1 + self.low_level_gains
        self.y2 = self.thresholds + (self.x2 - self.thresholds) / self.ratios

        self.alpha = (self.y2 - self.y1) / (self.x2 - self.x1)  # Slope of the knee region

        # Pre-compute constants for efficient processing
        self.const_one = 1 / self.ratios - 1  # Slope factor for compression
        self.const_two = self.thresholds - self.knee_width / 2  # Start of knee region
        self.const_three = self.knee_width * 2  # Full knee width for normalization

        self.gt0 = fmot.nn.Gt0()

    def forward(self, xG: torch.Tensor) -> torch.Tensor:
        """Apply dynamic range compression to input levels.

        Args:
            xG: Input levels in decibels.

        Returns:
            torch.Tensor: Gain values in decibels to be applied to the input.
        """
        # Separate regions:
        # low: xG < T - W/2
        # knee: |xG - T| <= W/2
        # high: xG > T + W/2
        low_level_region_mask = self.gt0(self.thresholds - self.knee_width / 2 - xG)
        compression_region_mask = self.gt0(xG - self.thresholds - self.knee_width / 2)
        knee_region_mask = 1 - (low_level_region_mask + compression_region_mask)

        yG_low = xG + self.low_level_gains
        yG_high = self.thresholds + (xG - self.thresholds) / self.ratios
        yG_knee = self.y1 + self.alpha * (xG - self.x1)

        yG = yG_low * low_level_region_mask + yG_high * compression_region_mask + yG_knee * knee_region_mask

        G = yG - xG
        return G


class WideDynamicRangeCompressor(nn.Module):
    def __init__(
        self,
        compress_thresh: list[float],
        compress_ratio: list[float],
        low_level_gain: list[float],
        knee_width: float,
        lim_thresh: float,
    ) -> None:
        super().__init__()
        self.compress_thresh = compress_thresh
        self.compress_ratio = compress_ratio
        self.lim_thresh = lim_thresh
        self.knee_width = knee_width

        self.compressor = DynamicRangeCompressor(
            thresholds=compress_thresh,
            knee_width=knee_width,
            ratios=compress_ratio,
            min_knee_width=2,
            low_level_gains=low_level_gain,
        )
        self.limiter = Limiter(threshold=lim_thresh, knee_width=knee_width, min_knee_width=2)

    def forward(self, xG: torch.Tensor) -> torch.Tensor:
        """

        Args:
            x: The input tensor in decibel scale.

        Returns:
            torch.Tensor: The gain tensor in decibel scale that should be applied to the input for WDRC.
        """
        # Apply DRC
        gain_db = self.compressor(xG)
        xG_compressed = gain_db + xG

        # Apply limiting
        gain_db = self.limiter(xG_compressed)
        xG_compressed = gain_db + xG_compressed

        # Find the Overall gain
        gain_overall_db = xG_compressed - xG
        return gain_overall_db


class WDRCModule(nn.Module):
    def __init__(
        self,
        sr: int,
        n_fft: int,
        n_mels: int,
        attack_time: float,
        release_time: float,
        delta_t: float,
        compress_thresh: list[float],
        compress_ratio: list[float],
        low_level_gain: list[float],
        lim_thresh: float,
        knee_width: float = 10,
        seq_len_dim: int = 1,
    ) -> None:
        """Wide Dynamic Range Compression (WDRC) module for audio processing.

        This module implements a complete WDRC processing pipeline:
        1. Convert STFT to mel-scale power spectrum for perceptual processing
        2. Apply temporal smoothing using AREMA
        3. Apply dynamic range compression and limiting in mel domain
        4. Convert gains back to STFT domain and apply to complex spectrum

        Args:
            sr: Audio sampling rate in Hz.
            n_fft: FFT size for spectral analysis.
            n_mels: Number of mel frequency bands for perceptual processing.
            attack_time: AREMA attack time in seconds for rising levels.
            release_time: AREMA release time in seconds for falling levels.
            delta_t: Time between frames in seconds (hop_size/sr).
            compress_thresh: Compression threshold in dB.
            compress_ratio: Compression ratio (input:output dB).
            lim_thresh: Limiting threshold in dB.
            knee_width: Width of knee region in dB for smooth transitions.
            low_level_gain: Gain applied to low-level signals (under threshold) in dB.
            seq_len_dim: Index of sequence length dimension in input tensor.
        """
        super().__init__()

        # Temporal smoothing for level estimation
        self.arema = AREMA(
            features=n_mels, dim=seq_len_dim, attack_time=attack_time, release_time=release_time, delta_t=delta_t
        )

        # Dynamic range processing
        self.wdrc = WideDynamicRangeCompressor(
            compress_thresh=compress_thresh,
            compress_ratio=compress_ratio,
            lim_thresh=lim_thresh,
            knee_width=knee_width,
            low_level_gain=low_level_gain,
        )

        # Spectral processing components
        self.magnitude = Magnitude()
        self.mel_transform = MelFilterBank(sr, n_fft, n_mels=n_mels, fmin=0.0)
        self.inv_mel_transform = InverseMelFilterBank(sr, n_fft, n_mels=n_mels, fmin=0.0, mode="transpose_stft_norm")

        # Constant for dB to linear conversion (20/ln(10))
        self.ln10_div_20 = 0.115

    def forward(self, stft_real_imag: torch.Tensor) -> torch.Tensor:
        """Process audio using WDRC in the spectral domain.

        Args:
            stft_real_imag: Complex STFT coefficients as concatenated real and imaginary parts. [b, t, 2 * n_fft]

        Returns:
            torch.Tensor: Processed STFT coefficients as concatenated real and imaginary parts. [b, t, 2 * n_fft]
        """
        # Split complex STFT into real and imaginary components
        stft_real, stft_imag = torch.chunk(stft_real_imag, chunks=2, dim=-1)

        # Convert to power spectrum in linear domain
        power_spec = self.magnitude(real=stft_real, imag=stft_imag)

        # Transform to mel-frequency scale for perceptual processing
        mel_fbank = self.mel_transform(power_spec)

        # Apply temporal smoothing to level estimates
        mfbank_fsema = self.arema(mel_fbank)

        # Convert to dB scale for compression processing
        log_mel_spectrogram = 20 * torch.log10(mfbank_fsema + 1e-6)

        # Calculate compression and limiting gains in dB
        wdrc_mel_gains_db = self.wdrc(log_mel_spectrogram)

        # Convert gains from dB to linear scale
        wdrc_mel_gains = torch.exp(self.ln10_div_20 * wdrc_mel_gains_db)

        # Convert gains from mel to STFT frequency scale
        wdrc_stft_gains = self.inv_mel_transform(wdrc_mel_gains)

        # Apply gains to complex STFT coefficients
        stft_real_enhanced = wdrc_stft_gains * stft_real
        stft_imag_enhanced = wdrc_stft_gains * stft_imag

        # Recombine real and imaginary parts
        stft_enhanced_real_imag = torch.cat([stft_real_enhanced, stft_imag_enhanced], dim=-1)

        return stft_enhanced_real_imag
