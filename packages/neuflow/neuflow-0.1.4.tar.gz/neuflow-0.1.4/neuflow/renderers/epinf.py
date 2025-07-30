# -*- coding: utf-8 -*-
"""
Author: Xiang Yangcheng [https://github.com/Xayah-Hina]
GitHub: https://github.com/IME-lab-Hokudai/EPINF-NeuFlow
Last Modification Date: 2025-07-10
Description: The pytorch implementation of the paper "Efficient Physics Informed Neural Reconstruction of Diverse Fluid Dynamics from Sparse Observations".
License: Mozilla Public License 2.0 (MPL-2.0)
Copyright (c) 2025 Xiang Yangcheng, IME Lab, Hokkaido University, Japan.
"""
import dataclasses
import typing

import torch

from .api import RendererAPI
from ..models import EPINFHybridModel
from ..plugins import TrainSpace, SparseLoss, ImageMaskLoss, HyFluidVelocityLoss, RGBAccConsistLoss


class EPINFRenderer(RendererAPI):
    @dataclasses.dataclass
    class Config:
        num_sample_rays: int = dataclasses.field(default=1024 * 2, metadata={'help': 'number of rays to sample per batch'})
        num_depth_samples: int = dataclasses.field(default=1024, metadata={'help': 'number of depth samples per ray'})
        num_importance_samples: int = dataclasses.field(default=0, metadata={'help': 'number of importance samples per ray'})
        use_normalized_directions: bool = dataclasses.field(default=True, metadata={'help': 'whether to use normalized directions for rendering'})
        chunk: int = dataclasses.field(default=1024 * 2, metadata={'help': 'chunk size for rendering'})

        normalized_directions: bool = dataclasses.field(default=True, metadata={'help': 'whether to use normalized directions for rendering'})
        importance_samples: bool = dataclasses.field(default=True, metadata={'help': 'whether to use importance sampling for rendering'})

    def __init__(self, cfg: Config):
        super().__init__(cfg=cfg)

        # ---------- PLUGINS ----------
        self.tsm: TrainSpace = TrainSpace(resolution=64)
        self.register_plugin(plugin=self.tsm)
        self.register_plugin(plugin=SparseLoss(max_level=3, delay_iters=300))
        self.register_plugin(plugin=ImageMaskLoss(delay_iters=300))
        # self.register_plugin(plugin=HyFluidVelocityLoss())
        # self.register_plugin(plugin=RGBAccConsistLoss(delay_iters=300))
        # ---------- PLUGINS ----------

        self.mode: typing.Literal['hybrid', 'dynamic', 'static'] = 'hybrid'
        self.set_mode(mode=self.mode)

    def set_mode(self, mode: typing.Literal['hybrid', 'dynamic', 'static']):
        if mode not in ['hybrid', 'dynamic', 'static', 'vel']:
            raise ValueError(f"Unknown mode: {mode}")
        self.mode = mode

    @property
    def num_sample_rays(self):
        return self.cfg.num_sample_rays

    @property
    def normalized_directions(self):
        return self.cfg.normalized_directions

    @property
    def chunk(self):
        return self.cfg.chunk

    def render_impl(self,
                    model: EPINFHybridModel,
                    rays_o: torch.Tensor,
                    rays_d: torch.Tensor,
                    nears: torch.Tensor,
                    fars: torch.Tensor,
                    pose_indices: torch.Tensor,
                    ):
        match self.mode:
            case 'hybrid':
                return self.render_hybrid(model=model, rays_o=rays_o, rays_d=rays_d, nears=nears, fars=fars, pose_indices=pose_indices)
            case 'dynamic':
                return self.render_dynamic(model=model, rays_o=rays_o, rays_d=rays_d, nears=nears, fars=fars, pose_indices=pose_indices)
            case 'static':
                return self.render_static(model=model, rays_o=rays_o, rays_d=rays_d, nears=nears, fars=fars, pose_indices=pose_indices)
            case _:
                raise ValueError(f"Unknown mode: {self.mode}")

    def render_hybrid(self,
                      model: EPINFHybridModel,
                      rays_o: torch.Tensor,
                      rays_d: torch.Tensor,
                      nears: torch.Tensor,
                      fars: torch.Tensor,
                      pose_indices: torch.Tensor,
                      ):
        num_sample_rays = rays_d.shape[0]

        xyz, z_vals = self.sample_points(
            rays_o=rays_o,
            rays_d=rays_d,
            nears=nears,
            fars=fars,
            num_depth_samples=self.cfg.num_depth_samples,
            use_perturb=model.training,
        )
        xyz_masked, mask = self.normalize_and_filter_xyz(xyz=xyz)
        view_dirs_masked = self.normalize_and_filter_view_dirs(view_dirs=rays_d, expand_shape=xyz.shape, mask=mask)

        if xyz_masked.numel() > 0:
            sigma_static_masked, geo_feat_static_masked = model.static_renderer.sigma(xyz_masked)
            sigma_dynamic_masked, geo_feat_dynamic_masked = model.dynamic_renderer.sigma(xyz_masked)
            sigma_static = self.assemble_masked_tensor(mask, sigma_static_masked, (num_sample_rays, self.cfg.num_depth_samples, 1))  # shape: (num_sample_rays, num_depth_samples, 1)
            sigma_dynamic = self.assemble_masked_tensor(mask, sigma_dynamic_masked, (num_sample_rays, self.cfg.num_depth_samples, 1))  # shape: (num_sample_rays, num_depth_samples, 1)

            rgb_static_masked = model.static_renderer.rgb(None, view_dirs_masked, geo_feat_static_masked)
            rgb_dynamic_masked = model.dynamic_renderer.rgb(None, view_dirs_masked, geo_feat_dynamic_masked)
            rgb_static = self.assemble_masked_tensor(mask, rgb_static_masked, (num_sample_rays, self.cfg.num_depth_samples, 3))  # shape: (num_sample_rays, num_depth_samples, 3)
            rgb_dynamic = self.assemble_masked_tensor(mask, rgb_dynamic_masked, (num_sample_rays, self.cfg.num_depth_samples, 3))  # shape: (num_sample_rays, num_depth_samples, 3)

            alpha_static = self.sigma_to_alpha(sigma=sigma_static, z_vals=z_vals)  # shape: (num_sample_rays, num_depth_samples)
            alpha_dynamic = self.sigma_to_alpha(sigma=sigma_dynamic, z_vals=z_vals)  # shape: (num_sample_rays, num_depth_samples)
            alpha_hybrid = 1 - (1.0 - alpha_static) * (1.0 - alpha_dynamic)  # shape: (num_sample_rays, num_depth_samples)

            eps = torch.finfo(alpha_hybrid.dtype).eps
            transmittance_hybrid = torch.cumprod(
                torch.cat([torch.ones_like(alpha_hybrid[:, :1]), 1. - alpha_hybrid + eps], dim=-1),
                dim=-1,
            )[:, :-1]  # shape: (num_sample_rays, num_depth_samples)
            weights_static = alpha_static * transmittance_hybrid  # shape: (num_sample_rays, num_depth_samples)
            weights_dynamic = alpha_dynamic * transmittance_hybrid  # shape: (num_sample_rays, num_depth_samples)

            acc_map = self.weights_to_acc_map(weights=weights_static) + self.weights_to_acc_map(weights=weights_dynamic)  # shape: (num_sample_rays,)
            depth_map = self.weights_to_depth_map(weights=weights_static, z_vals=z_vals, nears=nears, fars=fars) + self.weights_to_depth_map(weights=weights_dynamic, z_vals=z_vals, nears=nears, fars=fars)  # shape: (num_sample_rays,)
            rgb_map = self.weights_to_rgb_map(weights=weights_static, rgb=rgb_static) + self.weights_to_rgb_map(weights=weights_dynamic, rgb=rgb_dynamic)  # shape: (num_sample_rays, 3)
            rgb_map = rgb_map + (1 - acc_map).unsqueeze(-1) * self.background_color

            # ---------- PLUGINS ----------
            if self.training:
                self.tsm.update(xyz=xyz_masked, index=int(pose_indices[0].item()))
                for sl in filter(lambda v: isinstance(v, SparseLoss), self.plugins):
                    sl: SparseLoss
                    sl.compute(tsm=self.tsm, xyz=xyz_masked, sigma=sigma_static_masked + sigma_dynamic_masked)
            # ---------- PLUGINS ----------

        else:
            rgb_map = torch.zeros_like(rays_d)  # shape: (num_sample_rays, 3)
            depth_map = torch.zeros_like(rays_d[..., 0])  # shape: (num_sample_rays,)
            acc_map = torch.zeros_like(rays_d[..., 0])  # shape: (num_sample_rays,)

        ret_static = self.render_static(model, rays_o=rays_o, rays_d=rays_d, nears=nears, fars=fars, pose_indices=pose_indices)
        ret_dynamic = self.render_dynamic(model, rays_o=rays_o, rays_d=rays_d, nears=nears, fars=fars, pose_indices=pose_indices)

        return {
            "rgb_map": rgb_map,
            "depth_map": depth_map,
            "acc_map": acc_map,
            'rgb_map_static_independent': ret_static['rgb_map'],
            'depth_map_static_independent': ret_static['depth_map'],
            'acc_map_static_independent': ret_static['acc_map'],
            'rgb_map_dynamic_independent': ret_dynamic['rgb_map'],
            'depth_map_dynamic_independent': ret_dynamic['depth_map'],
            'acc_map_dynamic_independent': ret_dynamic['acc_map'],
        }

    def render_dynamic(self,
                       model: EPINFHybridModel,
                       rays_o: torch.Tensor,
                       rays_d: torch.Tensor,
                       nears: torch.Tensor,
                       fars: torch.Tensor,
                       pose_indices: torch.Tensor,
                       ):
        num_sample_rays = rays_d.shape[0]

        xyz, z_vals = self.sample_points(
            rays_o=rays_o,
            rays_d=rays_d,
            nears=nears,
            fars=fars,
            num_depth_samples=self.cfg.num_depth_samples,
            use_perturb=model.training,
        )
        xyz_masked, mask = self.normalize_and_filter_xyz(xyz=xyz)
        view_dirs_masked = self.normalize_and_filter_view_dirs(view_dirs=rays_d, expand_shape=xyz.shape, mask=mask)
        if xyz_masked.numel() > 0:
            sigma_ret = model.dynamic_renderer.sigma(xyz_masked)
            sigma_dynamic_masked, geo_feat_dynamic_masked = sigma_ret[0], sigma_ret[1]
            sigma_dynamic = self.assemble_masked_tensor(mask, sigma_dynamic_masked, (num_sample_rays, self.cfg.num_depth_samples, 1))  # shape: (num_sample_rays, num_depth_samples, 1)
            rgb_dynamic_masked = model.dynamic_renderer.rgb(None, view_dirs_masked, geo_feat_dynamic_masked)
            rgb_dynamic = self.assemble_masked_tensor(mask, rgb_dynamic_masked, (num_sample_rays, self.cfg.num_depth_samples, 3))  # shape: (num_sample_rays, num_depth_samples, 3)
            alpha_dynamic = self.sigma_to_alpha(sigma=sigma_dynamic, z_vals=z_vals)  # shape: (num_sample_rays, num_depth_samples)
            weights_dynamic_independent = self.alpha_to_weights(alpha=alpha_dynamic)
            acc_map_dynamic_independent = self.weights_to_acc_map(weights=weights_dynamic_independent)
            depth_map_dynamic_independent = self.weights_to_depth_map(weights=weights_dynamic_independent, z_vals=z_vals, nears=nears, fars=fars)
            rgb_map_dynamic_independent = self.weights_to_rgb_map(weights=weights_dynamic_independent, rgb=rgb_dynamic)
            rgb_map_dynamic_independent = rgb_map_dynamic_independent + (1 - acc_map_dynamic_independent).unsqueeze(-1) * self.background_color

            if self.training:
                for hvl in filter(lambda v: isinstance(v, HyFluidVelocityLoss), self.plugins):
                    hvl: HyFluidVelocityLoss
                    assert len(sigma_ret) == 4, "Expected sigma_ret to have 4 elements: (sigma_dynamic_masked, geo_feat_dynamic_masked, xyzt_encoded, xyzt)"
                    xyzt_encoded, xyzt = sigma_ret[2], sigma_ret[3]
                    hvl.compute(
                        xyzt=xyzt,
                        xyzt_encoded=xyzt_encoded,
                        sigma=sigma_dynamic_masked,
                        vel=model.vel_renderer.sigma_grad(xyzt_grad=xyzt),
                        fn=model.fn,
                    )
        else:
            rgb_map_dynamic_independent = torch.zeros_like(rays_d)  # shape: (num_sample_rays, 3)
            depth_map_dynamic_independent = torch.zeros_like(rays_d[..., 0])  # shape: (num_sample_rays,)
            acc_map_dynamic_independent = torch.zeros_like(rays_d[..., 0])  # shape: (num_sample_rays,)

        return {
            "rgb_map": rgb_map_dynamic_independent,
            "depth_map": depth_map_dynamic_independent,
            "acc_map": acc_map_dynamic_independent,
        }

    def render_static(self,
                      model: EPINFHybridModel,
                      rays_o: torch.Tensor,
                      rays_d: torch.Tensor,
                      nears: torch.Tensor,
                      fars: torch.Tensor,
                      pose_indices: torch.Tensor,
                      ):
        num_sample_rays = rays_d.shape[0]

        xyz, z_vals = self.sample_points(
            rays_o=rays_o,
            rays_d=rays_d,
            nears=nears,
            fars=fars,
            num_depth_samples=self.cfg.num_depth_samples,
            use_perturb=model.training,
        )
        xyz_masked, mask = self.normalize_and_filter_xyz(xyz=xyz)
        view_dirs_masked = self.normalize_and_filter_view_dirs(view_dirs=rays_d, expand_shape=xyz.shape, mask=mask)
        if xyz_masked.numel() > 0:
            sigma_static_masked, geo_feat_static_masked = model.static_renderer.sigma(xyz_masked)
            sigma_static = self.assemble_masked_tensor(mask, sigma_static_masked, (num_sample_rays, self.cfg.num_depth_samples, 1))  # shape: (num_sample_rays, num_depth_samples, 1)
            rgb_static_masked = model.static_renderer.rgb(None, view_dirs_masked, geo_feat_static_masked)
            rgb_static = self.assemble_masked_tensor(mask, rgb_static_masked, (num_sample_rays, self.cfg.num_depth_samples, 3))  # shape: (num_sample_rays, num_depth_samples, 3)
            alpha_static = self.sigma_to_alpha(sigma=sigma_static, z_vals=z_vals)  # shape: (num_sample_rays, num_depth_samples)
            weights_static_independent = self.alpha_to_weights(alpha=alpha_static)
            acc_map_static_independent = self.weights_to_acc_map(weights=weights_static_independent)
            depth_map_static_independent = self.weights_to_depth_map(weights=weights_static_independent, z_vals=z_vals, nears=nears, fars=fars)
            rgb_map_static_independent = self.weights_to_rgb_map(weights=weights_static_independent, rgb=rgb_static)
            rgb_map_static_independent = rgb_map_static_independent + (1 - acc_map_static_independent).unsqueeze(-1) * self.background_color

        else:
            rgb_map_static_independent = torch.zeros_like(rays_d)  # shape: (num_sample_rays, 3)
            depth_map_static_independent = torch.zeros_like(rays_d[..., 0])  # shape: (num_sample_rays,)
            acc_map_static_independent = torch.zeros_like(rays_d[..., 0])  # shape: (num_sample_rays,)

        return {
            "rgb_map": rgb_map_static_independent,
            "depth_map": depth_map_static_independent,
            "acc_map": acc_map_static_independent,
        }
