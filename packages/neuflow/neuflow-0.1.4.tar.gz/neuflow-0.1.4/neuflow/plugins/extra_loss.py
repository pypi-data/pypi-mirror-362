# -*- coding: utf-8 -*-
"""
Author: Xiang Yangcheng [https://github.com/Xayah-Hina]
GitHub: https://github.com/IME-lab-Hokudai/EPINF-NeuFlow
Last Modification Date: 2025-07-12
Description: The pytorch implementation of the paper "Efficient Physics Informed Neural Reconstruction of Diverse Fluid Dynamics from Sparse Observations".
License: Mozilla Public License 2.0 (MPL-2.0)
Copyright (c) 2025 Xiang Yangcheng, IME Lab, Hokkaido University, Japan.
"""
import torch

from .api import PluginLoss
from .train_sapce import TrainSpace


class ImageMaskLoss(PluginLoss):
    def __init__(self, delay_iters: int = 0, name: str = 'image_mask_loss'):
        super().__init__(name=name, weight=10000)
        self.delay_iters = delay_iters
        self.total_iters = 0

    def compute(self, rgb_map, acc_map, pixels_mask, background_color):
        self.total_iters += 1
        if self.total_iters < self.delay_iters:
            return

        masked_rgb_map = rgb_map[~pixels_mask]
        if masked_rgb_map.numel() > 0:
            masked_rgb_map = masked_rgb_map.view(-1, 3)
            background_color = background_color.view(1, 3)
            self._loss += torch.mean(torch.sum((masked_rgb_map - background_color) ** 2, dim=-1))
        masked_acc_map = acc_map[~pixels_mask]
        if masked_acc_map.numel() > 0:
            masked_acc_map = masked_acc_map.view(-1)
            self._loss += torch.mean(masked_acc_map)


class SparseLoss(PluginLoss):
    def __init__(self, max_level: int, delay_iters: int, name: str = 'sparse_loss'):
        super().__init__(name=name, weight=10000)
        assert max_level < 4, "max_level should be less than 4, as the maximum level in EPINF is 3."

        self.max_level = max_level
        self.delay_iters = delay_iters
        self.total_iters = 0

    def compute(self, tsm: TrainSpace, xyz: torch.Tensor, sigma: torch.Tensor):
        self.total_iters += 1
        if self.total_iters < self.delay_iters:
            return

        for level in range(self.max_level):
            sparse_mask = tsm.exclusive_n_mask(xyz=xyz, n=level + 1)
            sigma_sparse = sigma[sparse_mask]
            if sigma_sparse.numel() > 0:
                sparse_loss = 10.0 ** (-level) * sigma_sparse.mean()
                self._loss += sparse_loss


class RGBAccConsistLoss(PluginLoss):
    def __init__(self, delay_iters: int = 0, name: str = 'rgb_acc_consist_loss'):
        super().__init__(name=name, weight=10000)
        self.delay_iters = delay_iters
        self.total_iters = 0

    def compute(self, rgb_map, acc_map):
        self.total_iters += 1
        if self.total_iters < self.delay_iters:
            return

        if rgb_map.numel() > 0 and acc_map.numel() > 0:
            rgb_map_gray = rgb_map.mean(dim=-1, keepdim=True)
            rgb_map_gray_norm = rgb_map_gray / (rgb_map_gray.max() + 1e-6)
            acc_map_norm = acc_map / (acc_map.max() + 1e-6)
            proportional_loss = torch.mean((rgb_map_gray_norm - acc_map_norm) ** 2)
            grayscale_loss = torch.mean((rgb_map - rgb_map_gray) ** 2)
            self._loss += (proportional_loss + 0.1 * grayscale_loss)


class HyFluidVelocityLoss(PluginLoss):
    def __init__(self, delay_iters: int = 0, name: str = "hyfluid_velocity_loss"):
        super().__init__(name=name, weight=1)
        self.total_iters = 0
        self.delay_iters = delay_iters

    @staticmethod
    def get_minibatch_jacobian(y, x):
        """Computes the Jacobian of y wrt x assuming minibatch-mode.
        Args:
          y: (N, ...) with a total of D_y elements in ...
          x: (N, ...) with a total of D_x elements in ...
        Returns:
          The minibatch Jacobian matrix of shape (N, D_y, D_x)
        """
        assert y.shape[0] == x.shape[0]
        y = y.view(y.shape[0], -1)
        # Compute Jacobian row by row.
        jac = []
        for j in range(y.shape[1]):
            dy_j_dx = torch.autograd.grad(
                y[:, j],
                x,
                torch.ones_like(y[:, j], device=y.get_device()),
                retain_graph=True,
                create_graph=True,
            )[0].view(x.shape[0], -1)

            jac.append(torch.unsqueeze(dy_j_dx, 1))
        jac = torch.cat(jac, 1)
        return jac

    def compute(self, xyzt, xyzt_encoded, sigma, vel, fn):
        self.total_iters += 1

        if self.total_iters < self.delay_iters:
            return

        split_nse_wei = 0.001

        jac = torch.vmap(torch.func.jacrev(fn))(xyzt_encoded)
        jac = jac.contiguous()
        jac_x = self.get_minibatch_jacobian(xyzt_encoded, xyzt)
        jac_x = jac_x.contiguous()
        jac = jac @ jac_x

        _d_x, _d_y, _d_z, _d_t = [torch.squeeze(_, -1) for _ in jac.split(1, dim=-1)]

        _u_x, _u_y, _u_z, _u_t = None, None, None, None
        _u, _v, _w = vel.split(1, dim=-1)
        split_nse = _d_t + (_u * _d_x + _v * _d_y + _w * _d_z)
        nse_errors = torch.mean(torch.square(split_nse))

        viz_dens_mask = sigma.detach() > 0.1
        vel_norm = vel.norm(dim=-1, keepdim=True)
        min_vel_mask = vel_norm.detach() < 0.2 * sigma.detach()
        vel_reg_mask = min_vel_mask & viz_dens_mask
        min_vel_reg_map = (0.2 * sigma - vel_norm) * vel_reg_mask.float()
        min_vel_reg = min_vel_reg_map.pow(2).mean()

        zero_dens_mask = sigma.detach() < 1e-3
        keep_zero_map = vel_norm * zero_dens_mask.float()
        proj_loss = split_nse_wei * keep_zero_map.pow(2).mean()

        self._loss += nse_errors + 10 * min_vel_reg + proj_loss
