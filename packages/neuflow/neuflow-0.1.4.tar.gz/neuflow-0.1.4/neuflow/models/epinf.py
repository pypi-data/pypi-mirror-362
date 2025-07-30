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
import math

import tinycudann
import torch

from .api import ModelAPI


class EPINFStaticModel(ModelAPI):
    @dataclasses.dataclass
    class Config:
        num_layers_sigma: int = dataclasses.field(default=3, metadata={'help': 'number of layers for the sigma network'})
        hidden_dim_sigma: int = dataclasses.field(default=64, metadata={'help': 'hidden dimension for the sigma network'})
        num_layers_rgb: int = dataclasses.field(default=3, metadata={'help': 'number of layers for the RGB network'})
        hidden_dim_rgb: int = dataclasses.field(default=64, metadata={'help': 'hidden dimension for the RGB network'})
        geo_feat_dim: int = dataclasses.field(default=32, metadata={'help': 'geometric feature dimension'})
        num_layers_bg: int = dataclasses.field(default=3, metadata={'help': 'number of layers for the background network'})
        hidden_dim_bg: int = dataclasses.field(default=64, metadata={'help': 'hidden dimension for the background network'})
        use_background: bool = dataclasses.field(default=False, metadata={'help': 'whether to use background in the dataset'})

    def __init__(self, cfg: Config):
        super().__init__(cfg=cfg)

        bound = 1
        self.encoder_sigma = tinycudann.Encoding(
            n_input_dims=3,
            encoding_config={
                "otype": "HashGrid",
                "n_levels": 16,
                "n_features_per_level": 2,
                "log2_hashmap_size": 19,
                "base_resolution": 16,
                "per_level_scale": 2 ** (math.log2(2048 * bound / 16) / (16 - 1)),
            },
        )
        self.sigma_net = tinycudann.Network(
            n_input_dims=int(self.encoder_sigma.n_output_dims),
            n_output_dims=1 + cfg.geo_feat_dim,
            network_config={
                "otype": "FullyFusedMLP",
                "activation": "ReLU",
                "output_activation": "None",
                "n_neurons": cfg.hidden_dim_sigma,
                "n_hidden_layers": cfg.num_layers_sigma - 1,
            },
        )

        self.encoder_dir = tinycudann.Encoding(
            n_input_dims=3,
            encoding_config={
                "otype": "SphericalHarmonics",
                "degree": 4,
            },
        )
        self.color_net = tinycudann.Network(
            n_input_dims=int(self.encoder_dir.n_output_dims) + cfg.geo_feat_dim,
            n_output_dims=3,
            network_config={
                "otype": "FullyFusedMLP",
                "activation": "ReLU",
                "output_activation": "None",
                "n_neurons": cfg.hidden_dim_rgb,
                "n_hidden_layers": cfg.num_layers_rgb - 1,
            },
        )

        if cfg.use_background:
            self.encoder_bg = tinycudann.Encoding(
                n_input_dims=2,
                encoding_config={
                    "otype": "HashGrid",
                    "n_levels": 4,
                    "n_features_per_level": 2,
                    "log2_hashmap_size": 19,
                    "base_resolution": 16,
                    "per_level_scale": 2 ** (math.log2(2048 * bound / 4) / (4 - 1)),
                },
            )
            self.bg_net = tinycudann.Network(
                n_input_dims=int(self.encoder_dir.n_output_dims) + int(self.encoder_bg.n_output_dims),
                n_output_dims=3,
                network_config={
                    "otype": "FullyFusedMLP",
                    "activation": "ReLU",
                    "output_activation": "None",
                    "n_neurons": cfg.hidden_dim_bg,
                    "n_hidden_layers": cfg.num_layers_bg - 1,
                },
            )

    def sigma(self, xyz):
        xyz_encoded = self.encoder_sigma(xyz)
        h = self.sigma_net(xyz_encoded)
        sigma = torch.nn.functional.relu(h[..., :1])
        geo_feat = h[..., 1:]
        return sigma, geo_feat

    def rgb(self, xyz, view_dirs, geo_feat, cond=None):
        view_dirs_encoded = self.encoder_dir(view_dirs)
        h = self.color_net(torch.cat([view_dirs_encoded, geo_feat], dim=-1))
        rgb = torch.sigmoid(h)
        return rgb

    def background(self, sph, view_dirs):
        sph_encoded = self.encoder_bg(sph)
        view_dirs_encoded = self.encoder_dir(view_dirs)
        h = self.bg_net(torch.cat([view_dirs_encoded, sph_encoded], dim=-1))
        rgb_bg = torch.sigmoid(h)
        return rgb_bg


class EPINFDynamicModel(ModelAPI):
    @dataclasses.dataclass
    class Config:
        num_layers_sigma: int = dataclasses.field(default=3, metadata={'help': 'number of layers for the sigma network'})
        hidden_dim_sigma: int = dataclasses.field(default=64, metadata={'help': 'hidden dimension for the sigma network'})
        num_layers_rgb: int = dataclasses.field(default=3, metadata={'help': 'number of layers for the RGB network'})
        hidden_dim_rgb: int = dataclasses.field(default=64, metadata={'help': 'hidden dimension for the RGB network'})
        geo_feat_dim: int = dataclasses.field(default=32, metadata={'help': 'geometric feature dimension'})

    def __init__(self, cfg: Config):
        super().__init__(cfg=cfg)

        bound = 1
        self.encoder = tinycudann.Encoding(
            n_input_dims=4,
            encoding_config={
                "otype": "HashGrid",
                "n_levels": 16,
                "n_features_per_level": 2,
                "log2_hashmap_size": 19,
                "base_resolution": 16,
                "per_level_scale": 2 ** (math.log2(2048 * bound / 16) / (16 - 1)),
            },
        )

        self.sigma_net = tinycudann.Network(
            n_input_dims=int(self.encoder.n_output_dims),
            n_output_dims=1 + cfg.geo_feat_dim,
            network_config={
                "otype": "FullyFusedMLP",
                "activation": "ReLU",
                "output_activation": "None",
                "n_neurons": cfg.hidden_dim_sigma,
                "n_hidden_layers": cfg.num_layers_sigma - 1,
            },
        )

        self.encoder_dir = tinycudann.Encoding(
            n_input_dims=3,
            encoding_config={
                "otype": "SphericalHarmonics",
                "degree": 4,
            },
        )

        self.color_net = tinycudann.Network(
            n_input_dims=int(self.encoder_dir.n_output_dims) + cfg.geo_feat_dim,
            n_output_dims=3,
            network_config={
                "otype": "FullyFusedMLP",
                "activation": "ReLU",
                "output_activation": "None",
                "n_neurons": cfg.hidden_dim_rgb,
                "n_hidden_layers": cfg.num_layers_rgb - 1,
            },
        )

        self._time = None

    @property
    def time(self):
        assert self._time is not None
        assert isinstance(self._time, torch.Tensor)
        assert self._time.shape[0] == 1
        return self._time

    def set_time(self, time):
        self._time = time

    def sigma(self, xyz):
        xyzt = torch.cat([xyz, self.time.unsqueeze(0).expand_as(xyz[..., :1])], dim=-1)
        xyzt_encoded = self.encoder(xyzt)
        h = self.sigma_net(xyzt_encoded)
        sigma = torch.nn.functional.relu(h[..., :1])
        geo_feat = h[..., 1:]
        return sigma, geo_feat

    def rgb(self, xyz, view_dirs, geo_feat, cond=None):
        view_dirs_encoded = self.encoder_dir(view_dirs)
        h = self.color_net(torch.cat([view_dirs_encoded, geo_feat], dim=-1))
        rgb = torch.sigmoid(h)
        return rgb

    def background(self, sph, view_dirs):
        raise NotImplementedError("Background rendering is not implemented for dynamic models.")


class EPINFDynamicModelDoubleGradable(EPINFDynamicModel):
    def __init__(self, cfg: EPINFDynamicModel.Config):
        super().__init__(cfg)

        # Override the sigma network to allow double gradient computation
        sigma_net = []
        for l in range(cfg.num_layers_sigma):
            if l == 0:
                in_dim = self.encoder.n_output_dims
            else:
                in_dim = cfg.hidden_dim_sigma
            if l == cfg.num_layers_sigma - 1:
                out_dim = 1 + cfg.geo_feat_dim
            else:
                out_dim = cfg.hidden_dim_sigma
            sigma_net.append(torch.nn.Linear(in_dim, out_dim, bias=False))
        self.sigma_net = torch.nn.ModuleList(sigma_net)

    def sigma(self, xyz):
        xyzt = torch.cat([xyz, self.time.unsqueeze(0).expand_as(xyz[..., :1])], dim=-1)
        if self.training:
            xyzt.requires_grad = True
        xyzt_encoded = self.encoder(xyzt)

        h = xyzt_encoded
        for l in range(self.cfg.num_layers_sigma):
            h = self.sigma_net[l](h)
            if l != self.cfg.num_layers_sigma - 1:
                h = torch.nn.functional.relu(h, inplace=True)

        sigma = torch.nn.functional.relu(h[..., :1])
        geo_feat = h[..., 1:]
        return sigma, geo_feat, xyzt_encoded, xyzt

    def fn(self, hidden):
        h = hidden
        for l in range(self.cfg.num_layers_sigma):
            h = self.sigma_net[l](h)
            if l != self.cfg.num_layers_sigma - 1:
                h = torch.nn.functional.relu(h, inplace=True)
        return torch.nn.functional.relu(h[..., :1])


class EPINFVelocityModel(ModelAPI):
    @dataclasses.dataclass
    class Config:
        num_layers_vel_sigma: int = dataclasses.field(default=3, metadata={'help': 'number of layers for the sigma network'})
        hidden_dim_vel_sigma: int = dataclasses.field(default=64, metadata={'help': 'hidden dimension for the sigma network'})

    def __init__(self, cfg: Config):
        super().__init__(cfg=cfg)

        bound = 1
        self.encoder_vel = tinycudann.Encoding(
            n_input_dims=4,
            encoding_config={
                "otype": "HashGrid",
                "n_levels": 16,
                "n_features_per_level": 2,
                "log2_hashmap_size": 19,
                "base_resolution": 16,
                "per_level_scale": 2 ** (math.log2(2048 * bound / 16) / (16 - 1)),
            },
        )

        self.sigma_vel_net = tinycudann.Network(
            n_input_dims=int(self.encoder_vel.n_output_dims),
            n_output_dims=3,
            network_config={
                "otype": "FullyFusedMLP",
                "activation": "ReLU",
                "output_activation": "None",
                "n_neurons": cfg.hidden_dim_vel_sigma,
                "n_hidden_layers": cfg.num_layers_vel_sigma - 1,
            },
        )

        self._time = None

    @property
    def time(self):
        assert self._time is not None
        assert isinstance(self._time, torch.Tensor)
        assert self._time.shape[0] == 1
        return self._time

    def set_time(self, time):
        self._time = time

    def vel(self, xyz):
        return self.sigma(xyz)

    def sigma_grad(self, xyzt_grad):
        xyzt_encoded = self.encoder_vel(xyzt_grad)
        velocity = self.sigma_vel_net(xyzt_encoded)
        return velocity

    def sigma(self, xyz):
        xyzt = torch.cat([xyz, self.time.unsqueeze(0).expand_as(xyz[..., :1])], dim=-1)
        xyzt_encoded = self.encoder_vel(xyzt)
        velocity = self.sigma_vel_net(xyzt_encoded)
        return velocity


class EPINFHybridModel(ModelAPI):
    @dataclasses.dataclass
    class Config:
        static: EPINFStaticModel.Config = dataclasses.field(default_factory=EPINFStaticModel.Config, metadata={'help': 'Configuration for the static model'})
        dynamic: EPINFDynamicModel.Config = dataclasses.field(default_factory=EPINFDynamicModel.Config, metadata={'help': 'Configuration for the dynamic model'})
        vel: EPINFVelocityModel.Config = dataclasses.field(default_factory=EPINFVelocityModel.Config, metadata={'help': 'Configuration for the velocity model'})

        legacy: bool = dataclasses.field(default=False, metadata={'help': 'Whether to use legacy mode for the hybrid model'})

    def __init__(self, cfg: Config):
        super().__init__(cfg=cfg)
        self.static_renderer: EPINFStaticModel = EPINFStaticModel(cfg=cfg.static)
        self.dynamic_renderer: EPINFDynamicModel | EPINFDynamicModelDoubleGradable = EPINFDynamicModelDoubleGradable(cfg=cfg.dynamic) if cfg.legacy else EPINFDynamicModel(cfg=cfg.dynamic)
        self.vel_renderer: EPINFVelocityModel = EPINFVelocityModel(cfg=cfg.vel)

    @property
    def time(self):
        return self.dynamic_renderer.time

    def set_time(self, time):
        self.dynamic_renderer.set_time(time)
        self.vel_renderer.set_time(time)

    def sigma(self, xyz):
        ret_sta = self.static_renderer.sigma(xyz)
        ret_dyn = self.dynamic_renderer.sigma(xyz)
        sigma_static, geo_feat_static = ret_sta[0], ret_sta[1]
        sigma_dynamic, geo_feat_dynamic = ret_dyn[0], ret_dyn[1]
        return sigma_static + sigma_dynamic, geo_feat_static + geo_feat_dynamic

    def rgb(self, xyz, view_dirs, geo_feat, cond=None):
        raise NotImplementedError("Hybrid model does not support direct RGB rendering. Use static or dynamic renderer instead.")

    def vel(self, xyz):
        return self.vel_renderer.vel(xyz)

    def background(self, sph, view_dirs):
        raise NotImplementedError("Background rendering is not implemented for hybrid models. Use static or dynamic renderer instead.")
