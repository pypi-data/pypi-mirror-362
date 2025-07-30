from typing import List, Tuple

import torch
from fmot.nn import Cat, Sequencer, Split
from torch import Tensor


class MultiFrameBuffer(Sequencer):
    def __init__(self, feat_dim: int = 129):
        # t_m4, t_m3, t_m2, t_m1
        super().__init__(state_shapes=[[feat_dim * 2]] * 4, batch_dim=0, seq_dim=1)

        self.cat = Cat(dim=-1)
        self.split = Split(split_sizes=[feat_dim] * 6, dim=-1)
        self.split_ri = Split(split_sizes=[feat_dim, feat_dim], dim=-1)

    @torch.jit.export
    def step(self, x_t: Tensor, state: List[Tensor]) -> Tuple[Tensor, List[Tensor]]:
        """
        Args:
            x_t (Tensor): Deepfilter coefficients for the current step, shape [batch, feat_dim * 6].
            state (List[Tensor]): List of tensors representing the current state.

        Returns:
            Tuple[Tensor, List[Tensor]]: Output tensor and updated state. The tensor `x_t` is computed as a weighted
            sum of the previous states using the masks from `x_t`.
        """
        spec_m4, spec_m3, spec_m2, spec_m1 = state
        spec_m3_real, spec_m3_imag = self.split_ri(spec_m3)
        spec_m2_real, spec_m2_imag = self.split_ri(spec_m2)
        spec_m1_real, spec_m1_imag = self.split_ri(spec_m1)

        # x_t shape: [batch, feat_dim * 4]
        mask_m3, mask_m2, mask_m1, mask_t, spec_t_real, spec_t_imag = self.split(x_t)

        est_t_real = mask_m3 * spec_m3_real + mask_m2 * spec_m2_real + mask_m1 * spec_m1_real + mask_t * spec_t_real
        est_t_imag = mask_m3 * spec_m3_imag + mask_m2 * spec_m2_imag + mask_m1 * spec_m1_imag + mask_t * spec_t_imag

        est_t = self.cat([est_t_real, est_t_imag])

        state = [spec_m3, spec_m2, spec_m1, self.cat([spec_t_real, spec_t_imag])]

        return est_t, state
