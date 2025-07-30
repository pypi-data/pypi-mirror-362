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


class NGPModel(ModelAPI):
    @dataclasses.dataclass
    class Config:
        num_layers_sigma: int = dataclasses.field(default=2, metadata={'help': 'number of layers for the sigma network'})
        hidden_dim_sigma: int = dataclasses.field(default=64, metadata={'help': 'hidden dimension for the sigma network'})
        num_layers_rgb: int = dataclasses.field(default=3, metadata={'help': 'number of layers for the RGB network'})
        hidden_dim_rgb: int = dataclasses.field(default=64, metadata={'help': 'hidden dimension for the RGB network'})
        geo_feat_dim: int = dataclasses.field(default=15, metadata={'help': 'geometric feature dimension'})
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

    def forward(self, xyz, view_dirs):
        sigma, geo_feat = self.sigma(xyz)
        rgb = self.rgb(xyz, view_dirs, geo_feat)
        return sigma, rgb

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
        raise NotImplementedError("Background calculation is not implemented in NGPModel. This model does not support background rendering.")
