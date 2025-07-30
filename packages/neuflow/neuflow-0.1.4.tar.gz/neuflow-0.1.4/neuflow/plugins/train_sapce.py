# -*- coding: utf-8 -*-
"""
Author: Xiang Yangcheng [https://github.com/Xayah-Hina]
GitHub: https://github.com/IME-lab-Hokudai/EPINF-NeuFlow
Last Modification Date: 2025-07-10
Description: The pytorch implementation of the paper "Efficient Physics Informed Neural Reconstruction of Diverse Fluid Dynamics from Sparse Observations".
License: Mozilla Public License 2.0 (MPL-2.0)
Copyright (c) 2025 Xiang Yangcheng, IME Lab, Hokkaido University, Japan.
"""
import torch

from .api import Plugin


class TrainSpace(Plugin):
    def __init__(self, resolution: int, name: str = 'tsm'):
        super().__init__(name=name)
        self.register_buffer('trained_grids', torch.zeros((resolution, resolution, resolution), dtype=torch.int32))

        self.res = 256
        coords = torch.linspace(0, 1, steps=self.res + 1)
        centers = (coords[:-1] + coords[1:]) / 2
        x, y, z = torch.meshgrid(centers, centers, centers, indexing='ij')
        self.xyz = torch.stack([x, y, z], dim=-1).view(-1, 3)  # shape: (res^3, 1)

    def to(self, device):
        super().to(device)
        self.trained_grids = self.trained_grids.to(device=device)
        self.xyz = self.xyz.to(device=device)

    def update(self, xyz, index):
        assert xyz.max() <= 1.0 and xyz.min() >= 0.0, "Normalized xyz coordinates should be in [0, 1] range."
        assert index < 32, "Index must be less than 32."
        res = self.trained_grids.shape[0]  # Assuming trained_grids is a 4D tensor with shape (1, res, res, res)
        idx = (xyz * res).long().clamp(0, res - 1)
        x, y, z = idx[:, 0], idx[:, 1], idx[:, 2]

        bitmask = 1 << index
        before = self.trained_grids[x, y, z]
        changed = (before & bitmask) == 0
        self.trained_grids[x, y, z] = before | bitmask
        num_changed = changed.sum().item()
        return num_changed

    def exclusive_mask(self, xyz: torch.Tensor):
        pass

    def exclusive_grid(self):
        nonzero_mask = self.trained_grids != 0  # shape: (N, N, N)，bool
        # 初始化一个全 False 的 mask
        mask = torch.zeros_like(self.trained_grids, dtype=torch.bool)

        # 获取所有非零元素的索引
        indices = nonzero_mask.nonzero(as_tuple=False)  # shape: (M, 3)
        values = self.trained_grids[nonzero_mask]  # shape: (M,)

        # 判断是否是2的幂
        power_of_two_mask = (values & (values - 1)) == 0  # shape: (M,)

        # 只保留满足条件的位置
        selected_indices = indices[power_of_two_mask]  # shape: (K, 3)

        # 将这些位置设为 True
        mask[selected_indices[:, 0], selected_indices[:, 1], selected_indices[:, 2]] = True

        return mask  # shape: (N, N, N)，bool

    def exclusive_n_mask(self, xyz: torch.Tensor, n: int):
        res = self.trained_grids.shape[0]  # Assuming trained_grids is a 4D tensor with shape (1, res, res, res)
        idx = (xyz * res).long().clamp(0, res - 1)
        x, y, z = idx[:, 0], idx[:, 1], idx[:, 2]

        values = self.trained_grids[x, y, z]
        bit_counts = self.popcount32(values)
        mask = (bit_counts == n)
        return mask

    def exclusive_n_grid(self, n: int):
        assert 1 <= n <= 32
        grid = self.trained_grids  # shape: (res, res, res), dtype=torch.int32
        bit_counts = self.popcount32(grid)  # shape: (res, res, res), dtype=torch.int32
        mask = (bit_counts == n)  # shape: (res, res, res), dtype=torch.bool
        return mask

    def overlapped_grid(self):
        grid = self.trained_grids  # shape: (res, res, res), dtype=torch.int32
        bit_counts = self.popcount32(grid)  # 每个 voxel 有多少个 bit 被设置
        max_bits = bit_counts.max()  # 当前最大 bit 数
        mask = (bit_counts == max_bits)  # 哪些 voxel 的 bit 数是最大值
        return mask

    def empty_grid(self):
        return self.trained_grids == 0

    def occupied_grid(self):
        return self.trained_grids != 0

    @staticmethod
    def popcount32(x: torch.Tensor) -> torch.Tensor:
        """
        Bit-parallel population count for int32 tensor.
        Input: x (torch.int32 tensor)
        Output: int32 tensor of same shape, each value is the number of 1s in x[i].
        """
        x = x - ((x >> 1) & 0x55555555)
        x = (x & 0x33333333) + ((x >> 2) & 0x33333333)
        x = (x + (x >> 4)) & 0x0F0F0F0F
        x = (x * 0x01010101) >> 24
        return x
