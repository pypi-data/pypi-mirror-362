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


def advect_SL(q_grid, vel_world_prev, coord_3d_sim, dt, RK=1):
    """Advect a scalar quantity using a given velocity field.
    Args:
        q_grid: [X', Y', Z', C]
        vel_world_prev: [X, Y, Z, 3]
        coord_3d_sim: [X, Y, Z, 3]
        dt: float
        RK: int, number of Runge-Kutta steps
        y_start: where to start at y-axis
        proj_y: simulation domain resolution at y-axis
        use_project: whether to use Poisson solver
        project_solver: Poisson solver
        bbox_model: bounding box model
    Returns:
        advected_quantity: [X, Y, Z, 1]
        vel_world: [X, Y, Z, 3]
    """
    if RK == 1:
        vel_world = vel_world_prev.clone()
        vel_sim = vel_world  # [X, Y, Z, 3]
    elif RK == 2:
        vel_world = vel_world_prev.clone()  # [X, Y, Z, 3]
        # breakpoint()
        vel_sim = vel_world  # [X, Y, Z, 3]
        coord_3d_sim_midpoint = coord_3d_sim - 0.5 * dt * vel_sim  # midpoint
        midpoint_sampled = coord_3d_sim_midpoint * 2 - 1  # [X, Y, Z, 3]
        vel_sim = torch.nn.functional.grid_sample(vel_sim.permute(3, 2, 1, 0)[None], midpoint_sampled.permute(2, 1, 0, 3)[None], align_corners=True, padding_mode='zeros').squeeze(0).permute(3, 2, 1, 0)  # [X, Y, Z, 3]
    else:
        raise NotImplementedError
    backtrace_coord = coord_3d_sim - dt * vel_sim  # [X, Y, Z, 3]
    backtrace_coord_sampled = backtrace_coord * 2 - 1  # ranging [-1, 1]
    q_grid = q_grid[None, ...].permute([0, 4, 3, 2, 1])  # [N, C, Z, Y, X] i.e., [N, C, D, H, W]
    q_backtraced = torch.nn.functional.grid_sample(q_grid, backtrace_coord_sampled.permute(2, 1, 0, 3)[None, ...], align_corners=True, padding_mode='zeros')  # [N, C, D, H, W]
    q_backtraced = q_backtraced.squeeze(0).permute([3, 2, 1, 0])  # [X, Y, Z, C]
    return q_backtraced


def advect_maccormack(q_grid, vel_sim_prev, coord_3d_sim, dt):
    """
    Args:
        q_grid: [X', Y', Z', C]
        vel_world_prev: [X, Y, Z, 3]
        coord_3d_sim: [X, Y, Z, 3]
        dt: float
    Returns:
        advected_quantity: [X, Y, Z, C]
        vel_world: [X, Y, Z, 3]
    """
    q_grid_next = advect_SL(q_grid, vel_sim_prev, coord_3d_sim, dt)
    q_grid_back = advect_SL(q_grid_next, vel_sim_prev, coord_3d_sim, -dt)
    q_advected = q_grid_next + (q_grid - q_grid_back) / 2
    C = q_advected.shape[-1]
    for i in range(C):
        q_max, q_min = q_grid[..., i].max(), q_grid[..., i].min()
        q_advected[..., i] = q_advected[..., i].clamp_(q_min, q_max)
    return q_advected


def advect_density(den: torch.Tensor, vel: torch.Tensor, coord_3d_sim: torch.Tensor, dt: float, gt: torch.Tensor, gt_mask: torch.Tensor):
    den = advect_maccormack(den, vel, coord_3d_sim, dt)
    den[gt_mask] = gt[gt_mask]
    return den
