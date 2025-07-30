# -*- coding: utf-8 -*-
"""
Author: Xiang Yangcheng [https://github.com/Xayah-Hina]
GitHub: https://github.com/IME-lab-Hokudai/EPINF-NeuFlow
Last Modification Date: 2025-07-10
Description: The pytorch implementation of the paper "Efficient Physics Informed Neural Reconstruction of Diverse Fluid Dynamics from Sparse Observations".
License: Mozilla Public License 2.0 (MPL-2.0)
Copyright (c) 2025 Xiang Yangcheng, IME Lab, Hokkaido University, Japan.
"""
import rich
import torch

from ..models import ModelAPI
from ..plugins import Plugin, ImageMaskLoss, RGBAccConsistLoss


class RendererAPI(torch.nn.Module):
    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg

        self.render_width = 800  # Default render width, would be auto set to training image width
        self.render_height = 800  # Default render height, would be auto set to training image height
        self.min_near = 0.1
        self.max_far = 5.0

        self.register_buffer('aabb_std', torch.tensor([-1.0, -1.0, -1.0, 1.0, 1.0, 1.0]))  # [low_x, low_y, low_z, high_x, high_y, high_z]
        self.register_buffer('bound_std', torch.tensor([-1.0, -1.0, -1.0, 1.0, 1.0, 1.0]))  # [low_x, low_y, low_z, high_x, high_y, high_z]
        self.register_buffer('background_color', torch.tensor([0.0, 0.0, 0.0]))  # [r, g, b]

        self._plugins = []

    def register_plugin(self, plugin: Plugin):
        self.plugins.append(plugin)
        rich.print(f"[bold green]Registered plugin:[/bold green] {plugin.__class__.__name__}")

    @property
    def plugins(self):
        return self._plugins

    @property
    def num_sample_rays(self):
        raise NotImplementedError("The number of sample rays should be defined in the subclass.")

    @property
    def normalized_directions(self):
        raise NotImplementedError("The normalized directions should be defined in the subclass.")

    @property
    def chunk(self):
        raise NotImplementedError("The chunk size should be defined in the subclass.")

    def set_render_resolution(self, width: int, height: int):
        self.render_width = width
        self.render_height = height

    def set_min_near_far(self, min_near: float, max_far: float):
        self.min_near = min_near
        self.max_far = max_far

    def set_aabb_std(self, aabb_std: list):
        self.aabb_std = torch.tensor(aabb_std)

    def set_bound_std(self, bound_std: list):
        self.bound_std = torch.tensor(bound_std)

    def set_background_color(self, background_color: list):
        self.background_color = torch.tensor(background_color)

    def to(self, device):
        self.aabb_std = self.aabb_std.to(torch.float16).to(device=device)
        self.bound_std = self.bound_std.to(torch.float16).to(device=device)
        self.background_color = self.background_color.to(torch.float16).to(device=device)
        for plugin in self.plugins:
            plugin.to(device=device)

    def forward(self,
                model: ModelAPI,
                poses: torch.Tensor,  # shape: (N, 4, 4)
                focals: torch.Tensor | float,  # shape: (N) or float
                images: torch.Tensor | None,  # shape: (N, H, W, C) or None
                pose_indices: torch.Tensor | None,  # shape: (N) or None
                images_masks: torch.Tensor | None,  # shape: (N, H, W) or None
                ):
        N = poses.shape[0]
        W = images.shape[-2] if images is not None else self.render_width
        H = images.shape[-3] if images is not None else self.render_height

        rays_o, rays_d, pixels, pixels_mask = self.generate_rays(
            poses=poses,
            images=images,
            images_masks=images_masks,
            width=W,
            height=H,
            focals=focals,
            num_sample_rays=self.num_sample_rays if model.training else None,
            use_random_sampling=model.training,
            use_normalized_directions=self.normalized_directions,
        )

        rays_o_valid, rays_d_valid, nears_valid, fars_valid, hit_mask = self.ray_aabb_intersection(
            rays_o=rays_o,
            rays_d=rays_d,
            aabb=self.aabb_std,
            min_near=self.min_near,
            max_far=self.max_far,
        )
        num_rays = rays_d_valid.shape[0]
        if num_rays > 0:
            rendered_maps_list = []
            for start_idx in range(0, rays_d_valid.shape[0], self.chunk):
                ret = self.render_impl(
                    model=model,
                    rays_o=rays_o_valid[start_idx:start_idx + self.chunk],
                    rays_d=rays_d_valid[start_idx:start_idx + self.chunk],
                    nears=nears_valid[start_idx:start_idx + self.chunk],
                    fars=fars_valid[start_idx:start_idx + self.chunk],
                    pose_indices=pose_indices,
                )
                rendered_maps_list.append(ret)
            rendered_maps = self.merge_rendered_maps_list(rendered_maps_list)

            for key, value in rendered_maps.items():
                if value.ndim == 1:
                    value = value.unsqueeze(-1)  # Ensure value is at least 2D
                if model.training:
                    rendered_maps[key] = self.assemble_masked_tensor(mask_flat=hit_mask, tensor_masked_flat=value, shape=rays_o.shape[:-1] + value.shape[-1:])
                else:
                    rendered_maps[key] = self.assemble_masked_tensor(mask_flat=hit_mask, tensor_masked_flat=value, shape=(N, H, W) + value.shape[-1:])
        else:
            rendered_maps = {
                'rgb_map': torch.ones_like(rays_o) * self.background_color if model.training else torch.zeros((N, H, W, 3), dtype=poses.dtype, device=poses.device),
            }

        # ---------- PLUGINS ----------
        if self.training:
            if pixels_mask is not None:
                for iml in filter(lambda v: isinstance(v, ImageMaskLoss), self.plugins):
                    iml: ImageMaskLoss
                    iml.compute(rgb_map=rendered_maps['rgb_map'], acc_map=rendered_maps['acc_map'], pixels_mask=pixels_mask, background_color=self.background_color)
                for rgbcl in filter(lambda v: isinstance(v, RGBAccConsistLoss), self.plugins):
                    rgbcl: RGBAccConsistLoss
                    rgbcl.compute(rgb_map=pixels, acc_map=rendered_maps['acc_map'])
        # ---------- PLUGINS ----------

        if not model.training:
            if pixels is not None:
                pixels = pixels.reshape(N, H, W, -1)
            if pixels_mask is not None:
                pixels_mask = pixels_mask.reshape(N, H, W)

        return rendered_maps, pixels, pixels_mask

    def render_impl(self,
                    model: ModelAPI,
                    rays_o: torch.Tensor,
                    rays_d: torch.Tensor,
                    nears: torch.Tensor,
                    fars: torch.Tensor,
                    pose_indices: torch.Tensor,
                    ):
        raise NotImplementedError("The render_impl method should be implemented in a subclass.")

    def normalize_and_filter_xyz(self, xyz: torch.Tensor):
        aabb = self.aabb_std
        bound = self.bound_std

        low = aabb[:3]
        high = aabb[3:]
        scale = high - low
        xyz = (xyz - low) / scale

        xyz_flat = xyz.reshape(-1, 3)

        low_bound = (bound[:3] + 1.0) * 0.5  # Normalize to [0, 1]
        high_bound = (bound[3:] + 1.0) * 0.5  # Normalize to [0, 1]
        mask = ((xyz_flat >= low_bound) & (xyz_flat <= high_bound)).all(dim=-1)

        xyz_masked = xyz_flat[mask]
        return xyz_masked, mask

    @staticmethod
    def normalize_and_filter_view_dirs(view_dirs: torch.Tensor, expand_shape: torch.Size, mask: torch.Tensor):
        view_dirs = torch.nn.functional.normalize(view_dirs, dim=-1)
        view_dirs = (view_dirs + 1.0) * 0.5  # tcnn SH encoding requires inputs to be in [0, 1]
        view_dirs_exp = view_dirs.unsqueeze(1).expand(expand_shape)
        view_dirs_masked = view_dirs_exp.reshape(-1, 3)[mask]
        return view_dirs_masked

    @staticmethod
    def generate_rays(poses: torch.Tensor,  # shape: (N, 4, 4)
                      images: torch.Tensor | None,  # shape: (N, H, W, C) or None
                      images_masks: torch.Tensor | None,  # shape: (N, H, W) or None
                      width: int,
                      height: int,
                      focals: torch.Tensor | float,  # shape: (N) or float
                      num_sample_rays: int | None,
                      use_random_sampling: bool,
                      use_normalized_directions: bool,
                      ):
        device = poses.device
        dtype = poses.dtype
        N = poses.shape[0]

        if num_sample_rays is None:
            u, v = torch.meshgrid(torch.linspace(0, width - 1, width, device=device, dtype=dtype), torch.linspace(0, height - 1, height, device=device, dtype=dtype), indexing='xy')
            u = u.reshape(-1)  # shape: (width * height,)
            v = v.reshape(-1)  # shape: (width * height,)
        else:
            u = torch.randint(0, width, (num_sample_rays,), device=device, dtype=dtype)
            v = torch.randint(0, height, (num_sample_rays,), device=device, dtype=dtype)

        if use_random_sampling:
            u = u + torch.rand_like(u)
            v = v + torch.rand_like(v)

        if images is not None:
            grid_u = (u / (width - 1)) * 2 - 1
            grid_v = (v / (height - 1)) * 2 - 1
            grid = torch.stack([grid_u, grid_v], dim=-1)  # shape: (num_sample_rays, 2)
            grid = grid[None, :, None, :].expand(N, -1, 1, 2)  # shape: (N, num_sample_rays, 1, 2)
            images = torch.nn.functional.grid_sample(images.permute(0, 3, 1, 2), grid, mode='bilinear', align_corners=False).permute(0, 2, 1, 3).squeeze(-1)  # (N, C, H, W) x (N, num_sample_rays, 1, 2) -> (N, C, num_sample_rays, 1) -> (N, num_sample_rays, C, 1)
            if images_masks is not None:
                images_masks = images_masks.unsqueeze(-1).to(torch.float32)
                images_masks = torch.nn.functional.grid_sample(images_masks.permute(0, 3, 1, 2), grid, mode='bilinear', align_corners=False).permute(0, 2, 1, 3).squeeze(-1)  # (N, 1, H, W) x (N, num_sample_rays, 1, 2) -> (N, 1, num_sample_rays, 1) -> (N, num_sample_rays, 1, 1)
                images_masks = images_masks.squeeze(-1).to(torch.bool)  # shape: (N, num_sample_rays)

        focal = focals.item() if isinstance(focals, torch.Tensor) else focals  # TODO: support separate focal lengths for each pose
        u = (u - 0.5 * width) / focal  # shape: (num_sample_rays,)
        v = (v - 0.5 * height) / focal  # shape: (num_sample_rays,)
        dirs = torch.stack([u, -v, -torch.ones_like(u)], dim=-1)  # shape: (num_sample_rays, 3), OpenGL Style Camera
        if use_normalized_directions:
            dirs = torch.nn.functional.normalize(dirs, dim=-1)

        rays_d = torch.einsum('bij, bnj->bni', poses[:, :3, :3], dirs[None, :, :])  # shape: (N, num_sample_rays, 3)
        rays_o = poses[:, None, :3, 3].expand_as(rays_d)  # shape: (N, num_sample_rays, 3)

        rays_o = rays_o.contiguous().view(-1, 3)
        rays_d = rays_d.contiguous().view(-1, 3)
        pixels = images.contiguous().view(-1, images.shape[-1]) if images is not None else None  # shape: (N * num_sample_rays, 3)
        pixels_mask = images_masks.contiguous().flatten() if images_masks is not None else None  # shape: (N * num_sample_rays,)
        return rays_o, rays_d, pixels, pixels_mask

    @staticmethod
    def ray_aabb_intersection(rays_o, rays_d, aabb, min_near, max_far):
        """
        :param rays_o: (N, 3) Tensor, ray origins
        :param rays_d: (N, 3) Tensor, ray directions
        :param aabb: (6) Tensor or list, [low_x, low_y, low_z, high_x, high_y, high_z]
        :param min_near: Tensor, minimum near distance
        :param max_far: Tensor, maximum far distance
        :return: nears (N), fars (N), hit_mask (N) bool
        """
        import torch

        # 拆分 AABB
        aabb = aabb.to(rays_o.dtype).to(rays_o.device)
        low = aabb[:3]  # (3,)
        high = aabb[3:]  # (3,)

        # 避免除以0
        rays_d_safe = rays_d.clone()
        rays_d_safe[rays_d_safe == 0] = 1e-6

        # 计算每个维度的交点 t
        t_min = (low - rays_o) / rays_d_safe
        t_max = (high - rays_o) / rays_d_safe

        t1 = torch.minimum(t_min, t_max)  # (N, 3)
        t2 = torch.maximum(t_min, t_max)  # (N, 3)

        # 射线与 AABB 的进入和离开距离
        nears = t1.max(dim=-1).values  # (N,)
        fars = t2.min(dim=-1).values  # (N,)

        # 原始命中判断
        hit_mask = (fars >= nears) & (fars >= 0)

        # 应用 min_near 限制
        nears = nears.clamp(min=min_near)

        # 应用 max_far 限制
        fars = fars.clamp(max=max_far)

        # 如果 nears 提高后超过 fars，则不再命中
        hit_mask = hit_mask & (nears <= fars)

        rays_o_masked = rays_o[hit_mask]
        rays_d_masked = rays_d[hit_mask]
        nears_masked = nears[hit_mask]
        fars_masked = fars[hit_mask]

        return rays_o_masked, rays_d_masked, nears_masked, fars_masked, hit_mask

    @staticmethod
    def sample_points(rays_o: torch.Tensor, rays_d: torch.Tensor, nears: torch.Tensor, fars: torch.Tensor, num_depth_samples: int, use_perturb: bool):
        device = rays_d.device
        dtype = rays_d.dtype
        n_rays = rays_d.shape[0]

        # sample z vals
        num_rays = nears.shape[0]
        nears_exp = nears.unsqueeze(-1).expand(num_rays, num_depth_samples)  # [n_rays, n_depth_samples]
        fars_exp = fars.unsqueeze(-1).expand(num_rays, num_depth_samples)  # [n_rays, n_depth_samples]

        t_vals = torch.linspace(0., 1., steps=num_depth_samples, dtype=dtype, device=device)  # [n_depth_samples,]
        t_vals_exp = t_vals.unsqueeze(0).expand(num_rays, num_depth_samples)  # [n_rays, n_depth_samples]
        z_vals = nears_exp * (1. - t_vals_exp) + fars_exp * t_vals_exp  # [n_rays, n_depth_samples]
        if use_perturb:
            mid = 0.5 * (z_vals[..., 1:] + z_vals[..., :-1])  # [n_rays, n_depth_samples-1]
            upper = torch.cat([mid, z_vals[..., -1:]], dim=-1)  # [n_rays, n_depth_samples]
            lower = torch.cat([z_vals[..., :1], mid], dim=-1)  # [n_rays, n_depth_samples]
            t_rand = torch.rand_like(z_vals, dtype=dtype, device=device)  # [n_rays, n_depth_samples]
            z_vals = lower + (upper - lower) * t_rand  # [n_rays, n_depth_samples]

        z_vals_exp = z_vals.unsqueeze(-1).expand(n_rays, num_depth_samples, 1)  # shape: (n_rays, num_depth_samples, 1)
        rays_o_exp = rays_o.unsqueeze(1).expand(n_rays, num_depth_samples, 3)  # shape: (n_rays, num_depth_samples, 3)
        rays_d_exp = rays_d.unsqueeze(1).expand(n_rays, num_depth_samples, 3)  # shape: (n_rays, num_depth_samples, 3)

        pts = rays_o_exp + rays_d_exp * z_vals_exp  # shape: (n_rays, num_depth_samples, 3)

        return pts, z_vals_exp

    @staticmethod
    def assemble_masked_tensor(mask_flat, tensor_masked_flat, shape):
        device = tensor_masked_flat.device
        dtype = tensor_masked_flat.dtype
        tensor_flat = torch.zeros(shape, device=device, dtype=dtype).reshape(-1, shape[-1])
        tensor_flat[mask_flat] = tensor_masked_flat
        tensor = tensor_flat.reshape(shape)
        return tensor

    @staticmethod
    def merge_rendered_maps_list(rendered_maps_list: list[dict]) -> dict:
        assert len(rendered_maps_list) > 0, "列表不能为空"

        keys = rendered_maps_list[0].keys()
        # 检查所有 dict 的 key 是否一致
        for maps in rendered_maps_list:
            assert maps.keys() == keys, "所有 rendered_maps 的 key 必须一致"

        merged = {key: torch.cat([maps[key] for maps in rendered_maps_list], dim=0) for key in keys}
        return merged

    @staticmethod
    def sigma_to_alpha(sigma: torch.Tensor, z_vals: torch.Tensor):
        """
        :param sigma: [n_rays, n_depth_samples, 1] tensor representing the density.
        :param z_vals: [n_rays, n_depth_samples, 1] tensor representing the z-values (depth samples).
        :return: alpha: [n_rays, n_depth_samples] tensor representing the alpha values.
        """
        z_vals = z_vals.squeeze(-1)  # [n_rays, n_depth_samples]
        dists = z_vals[..., 1:] - z_vals[..., :-1]  # [n_rays, n_depth_samples-1]
        dists = torch.cat([dists, dists[..., -1:]], -1)  # [n_rays, n_depth_samples]
        alpha = 1.0 - torch.exp(-sigma.squeeze(-1) * dists)
        return alpha

    @staticmethod
    def alpha_to_weights(alpha: torch.Tensor):
        """
        :param alpha: [n_rays, n_depth_samples] tensor representing the alpha values.
        :return: weights: [n_rays, n_depth_samples] tensor representing the weights.
        """
        eps = torch.finfo(alpha.dtype).eps
        transmittance = torch.cumprod(
            torch.cat([torch.ones_like(alpha[:, :1]), 1. - alpha + eps], dim=-1),
            dim=-1,
        )[:, :-1]
        weights = alpha * transmittance
        return weights

    @staticmethod
    def weights_to_acc_map(weights: torch.Tensor):
        """
        :param weights: [n_rays, n_depth_samples] tensor representing the weights.
        :return: acc_map: [n_rays] tensor representing the accumulated weights.
        """
        acc_map = torch.sum(weights, dim=-1)
        return acc_map

    @staticmethod
    def weights_to_rgb_map(weights: torch.Tensor, rgb: torch.Tensor):
        """
        :param weights: [n_rays, n_depth_samples] tensor representing the weights.
        :param rgb: [n_rays, n_depth_samples, 3] or [1,] tensor representing the RGB values.
        :return: rgb_map: [n_rays, 3] tensor representing the RGB map.
        """
        rgb_map = torch.sum(weights.unsqueeze(-1) * rgb, dim=1)
        return rgb_map

    @staticmethod
    def weights_to_depth_map(weights: torch.Tensor, z_vals: torch.Tensor, nears, fars):
        """
        :param weights: [n_rays, n_depth_samples] tensor representing the weights.
        :param z_vals: [n_rays, n_depth_samples, 1] tensor representing the z-values (depth samples).
        :param nears: [n_rays] tensor representing the near plane distance.
        :param fars: [n_rays] tensor representing the far plane distance.
        :return: depth_map: [n_rays] tensor representing the depth map.
        """
        z_vals = z_vals.squeeze(-1)  # [n_rays, n_depth_samples]
        ori_z_vals = ((z_vals - nears.unsqueeze(-1).expand_as(z_vals)) / (fars.unsqueeze(-1).expand_as(z_vals) - nears.unsqueeze(-1).expand_as(z_vals))).clamp(0, 1)
        # eps = torch.finfo(weights.dtype).eps
        # weights_sum = torch.sum(weights, dim=-1) + eps
        # depth_map = torch.sum(weights * ori_z_vals, dim=-1) / weights_sum
        depth_map = torch.sum(weights * ori_z_vals, dim=-1)
        return depth_map
