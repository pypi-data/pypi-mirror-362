# -*- coding: utf-8 -*-
"""
Author: Xiang Yangcheng [https://github.com/Xayah-Hina]
GitHub: https://github.com/IME-lab-Hokudai/EPINF-NeuFlow
Last Modification Date: 2025-07-10
Description: The pytorch implementation of the paper "Efficient Physics Informed Neural Reconstruction of Diverse Fluid Dynamics from Sparse Observations".
License: Mozilla Public License 2.0 (MPL-2.0)
Copyright (c) 2025 Xiang Yangcheng, IME Lab, Hokkaido University, Japan.
"""
import os
import typing

import lightning
import torch


class PIDataset(torch.utils.data.Dataset):
    """
    PRIVATE CLASS
    - This class and its subclasses are only used inside datasets package.
    """

    @property
    def images(self):
        raise NotImplementedError("This method should be implemented in subclasses.")

    @property
    def images_highlighted(self):
        raise NotImplementedError("This method should be implemented in subclasses.")

    @property
    def images_masks(self):
        raise NotImplementedError("This method should be implemented in subclasses.")

    @property
    def poses(self):
        raise NotImplementedError("This method should be implemented in subclasses.")

    @property
    def focal(self):
        raise NotImplementedError("This method should be implemented in subclasses.")

    @property
    def width(self):
        raise NotImplementedError("This method should be implemented in subclasses.")

    @property
    def height(self):
        raise NotImplementedError("This method should be implemented in subclasses.")

    @property
    def near(self):
        raise NotImplementedError("This method should be implemented in subclasses.")

    @property
    def far(self):
        raise NotImplementedError("This method should be implemented in subclasses.")

    @property
    def num_poses(self):
        raise NotImplementedError("This method should be implemented in subclasses.")

    @property
    def num_times(self):
        raise NotImplementedError("This method should be implemented in subclasses.")

    def transform(self, translate, scale):
        raise NotImplementedError("This method should be implemented in subclasses.")


class PIDatasetAPI(lightning.LightningDataModule):
    """
    PUBLIC API:
        dataset_path: str
        aabb_std: list[min_x, min_y, min_z, max_x, max_y, max_z]
        bound_std: list[min_x, min_y, min_z, max_x, max_y, max_z]
        background_color: list[r, g, b]
        complex_background: bool
        num_train_poses: int
    """

    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg

        self.dataset_train: PIDataset | None = None
        self.dataset_val: PIDataset | None = None
        self.dataset_test: PIDataset | None = None

    def prepare_data(self):
        raise NotImplementedError("This method should be implemented in subclasses.")

    def setup(self, stage: str):
        if stage == 'fit':
            self.dataset_train = self.dataset('train')
            self.dataset_val = self.dataset('val')
        elif stage == 'validate':
            self.dataset_val = self.dataset('val')
        elif stage == 'test' or stage == 'predict':
            self.dataset_test = self.dataset('test')
        else:
            raise NotImplementedError('Unsupported stage: {}'.format(stage))

    def dataset(self, dataset_type: typing.Literal['train', 'val', 'test']) -> PIDataset:
        raise NotImplementedError("This method should be implemented in subclasses.")

    @staticmethod
    def collate(batch: list):
        raise NotImplementedError("This method should be implemented in subclasses.")

    def train_dataloader(self):
        return torch.utils.data.DataLoader(
            self.dataset_train,
            batch_size=1,
            shuffle=True,
            num_workers=min(os.cpu_count() - 1, 4),
            persistent_workers=True,
            collate_fn=self.collate,
        )

    def val_dataloader(self):
        return torch.utils.data.DataLoader(
            self.dataset_val,
            batch_size=1,
            shuffle=False,
            num_workers=min(os.cpu_count() - 1, 4),
            persistent_workers=True,
            collate_fn=self.collate,
        )

    def test_dataloader(self):
        return torch.utils.data.DataLoader(
            self.dataset_test,
            batch_size=1,
            shuffle=False,
            num_workers=min(os.cpu_count() - 1, 4),
            persistent_workers=True,
            collate_fn=self.collate,
        )

    def predict_dataloader(self):
        return self.test_dataloader()

    @property
    def pre_translate(self):
        raise NotImplementedError("This method should be implemented in subclasses.")

    @property
    def pre_scale(self):
        raise NotImplementedError("This method should be implemented in subclasses.")

    @property
    def aabb_std(self):
        raise NotImplementedError("This method should be implemented in subclasses.")

    @property
    def bound_std(self):
        raise NotImplementedError("This method should be implemented in subclasses.")

    @property
    def background_color(self):
        raise NotImplementedError("This method should be implemented in subclasses.")

    @property
    def complex_background(self):
        raise NotImplementedError("This method should be implemented in subclasses.")

    @property
    def num_train_poses(self):
        assert self.dataset_train is not None, "Dataset for training is not set up."
        return self.dataset_train.num_poses

    @property
    def width(self):
        assert self.dataset_train is not None, "Dataset for training is not set up."
        return self.dataset_train.width

    @property
    def height(self):
        assert self.dataset_train is not None, "Dataset for training is not set up."
        return self.dataset_train.height

    @property
    def near_std(self):
        assert self.dataset_train is not None, "Dataset for training is not set up."
        return self.dataset_train.near

    @property
    def far_std(self):
        assert self.dataset_train is not None, "Dataset for training is not set up."
        return self.dataset_train.far
