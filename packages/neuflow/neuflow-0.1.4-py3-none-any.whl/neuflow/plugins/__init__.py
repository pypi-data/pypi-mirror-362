# -*- coding: utf-8 -*-
"""
Author: Xiang Yangcheng [https://github.com/Xayah-Hina]
GitHub: https://github.com/IME-lab-Hokudai/EPINF-NeuFlow
Last Modification Date: 2025-07-10
Description: The pytorch implementation of the paper "Efficient Physics Informed Neural Reconstruction of Diverse Fluid Dynamics from Sparse Observations".
License: Mozilla Public License 2.0 (MPL-2.0)
Copyright (c) 2025 Xiang Yangcheng, IME Lab, Hokkaido University, Japan.
"""
from .api import Plugin, PluginLoss
from .extra_loss import ImageMaskLoss, SparseLoss, RGBAccConsistLoss, HyFluidVelocityLoss
from .train_sapce import TrainSpace

__all__ = ['Plugin', 'PluginLoss', 'TrainSpace', 'SparseLoss', 'ImageMaskLoss', 'RGBAccConsistLoss', 'HyFluidVelocityLoss']
