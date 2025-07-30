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


class ModelAPI(torch.nn.Module):
    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg

    def sigma(self, xyz):
        raise NotImplementedError("Sigma calculation is not implemented in the base API class. Please implement this method in a subclass.")

    def rgb(self, xyz, view_dirs, geo_feat, cond=None):
        raise NotImplementedError("RGB calculation is not implemented in the base API class. Please implement this method in a subclass.")

    def background(self, sph, view_dirs):
        raise NotImplementedError("Background calculation is not implemented in the base API class. Please implement this method in a subclass.")
