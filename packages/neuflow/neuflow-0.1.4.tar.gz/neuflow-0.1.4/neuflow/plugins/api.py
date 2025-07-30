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


class Plugin(torch.nn.Module):
    def __init__(self, name: str):
        super().__init__()
        self._name = name

    @property
    def name(self):
        return self._name

    def on_iter_start(self):
        pass

    def to(self, device):
        pass


class PluginLoss(Plugin):
    def __init__(self, name: str, weight):
        super().__init__(name)
        self._loss = torch.tensor(0.0)
        self._weight = weight
        self._enable = True

    def enable(self, enable: bool = True):
        self._enable = enable

    @property
    def loss(self):
        return self._loss

    @property
    def weight(self):
        return self._weight

    def on_iter_start(self):
        self._loss = torch.tensor(0.0, device=self._loss.device)

    def to(self, device):
        super().to(device)
        self._loss = self._loss.to(device=device)
