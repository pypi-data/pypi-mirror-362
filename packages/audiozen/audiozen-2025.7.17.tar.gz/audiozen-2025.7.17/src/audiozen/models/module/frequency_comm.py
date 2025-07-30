import math
from typing import List, Tuple

import torch
import torch.nn as nn
from fmot.nn import Cat, Chunk, Sequencer, SuperStructure, get_nonlin
from torch import Tensor


class FrequencyCommunicationOneStep(SuperStructure):
    def __init__(self, d_band: int, hidden_size: int, num_bands: int):
        super().__init__()
        self.linear_ih = nn.Linear(d_band, 3 * hidden_size, bias=True)
        self.linear_hh = nn.Linear(hidden_size, 3 * hidden_size, bias=True)

        # For backward direction (if bidirectional)
        self.linear_ih_back = nn.Linear(d_band, 3 * hidden_size, bias=True)
        self.linear_hh_back = nn.Linear(hidden_size, 3 * hidden_size, bias=True)

        # Output projection to combine forward and backward
        self.output_proj = nn.Linear(2 * hidden_size, num_bands * d_band)

        self.sigmoid_r = get_nonlin("sigmoid")
        self.sigmoid_z = get_nonlin("sigmoid")
        self.tanh = get_nonlin("tanh")

        self.num_bands = num_bands

        self.hf = nn.Parameter(torch.zeros(1, hidden_size), requires_grad=False)
        self.hb = nn.Parameter(torch.zeros(1, hidden_size), requires_grad=False)

        self.cat = Cat(dim=-1)
        self.chunk = Chunk(chunks=num_bands, dim=-1)
        self.chunk_3 = Chunk(chunks=3, dim=-1)

        k = math.sqrt(1 / hidden_size)
        for name, param in self.named_parameters():
            torch.nn.init.uniform_(param, -k, k)

    def forward(self, x_t: Tensor) -> Tensor:
        """
        Args:
            x_t: [batch, num_bands * d_band]

        Returns:
            Combined hidden state after processing in both directions
        """
        band_list = self.chunk(x_t)

        # Forward direction (low to high frequency)
        h_f = self.hf
        for i, xf in enumerate(band_list):
            stacked_layer_i = self.linear_ih(xf)
            stacked_layer_h = self.linear_hh(h_f)

            r_t, z_t, n_t = self.chunk_3(stacked_layer_i)
            r_t_h, z_t_h, n_t_h = self.chunk_3(stacked_layer_h)

            r_t = self.sigmoid_r(r_t + r_t_h)
            z_t = self.sigmoid_z(z_t + z_t_h)
            n_t = self.tanh(n_t + r_t * n_t_h)

            h_f = (1 - z_t) * n_t + z_t * h_f

        # Backward direction (high to low frequency)
        band_list = band_list[::-1]  # Reverse the list for backward processing
        h_b = self.hb
        for i, xf in enumerate(band_list):
            stacked_layer_i = self.linear_ih_back(xf)
            stacked_layer_h = self.linear_hh_back(h_b)

            r_t, z_t, n_t = self.chunk_3(stacked_layer_i)
            r_t_h, z_t_h, n_t_h = self.chunk_3(stacked_layer_h)

            r_t = self.sigmoid_r(r_t + r_t_h)
            z_t = self.sigmoid_z(z_t + z_t_h)
            n_t = self.tanh(n_t + r_t * n_t_h)

            h_b = (1 - z_t) * n_t + z_t * h_b

        # Combine forward and backward hidden states
        combined = self.cat([h_f, h_b])

        return self.output_proj(combined)


class FrequencyCommunication(Sequencer):
    def __init__(
        self,
        num_bands: int,
        d_band: int,
        hidden_size: int,
    ):
        super().__init__([[num_bands * d_band]], batch_dim=0, seq_dim=1)

        self.frequency_comm_one_step = FrequencyCommunicationOneStep(
            d_band=d_band,
            hidden_size=hidden_size,
            num_bands=num_bands,
        )

    @torch.jit.export
    def step(self, x_t: Tensor, state: List[Tensor]) -> Tuple[Tensor, List[Tensor]]:
        """

        Args:
            x_t: current input tensor, shape [batch, num_bands * d_band]
            state: _description_

        Returns:
            _description_
        """
        (h,) = state  # Unused in this implementation, but kept for compatibility
        x_out = self.frequency_comm_one_step(x_t)
        return x_out, [h]  # Update state with the new output
