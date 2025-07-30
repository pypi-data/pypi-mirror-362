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
import json
import os
import typing

import rich.progress
import torch
import torchvision

from .api import PIDataset, PIDatasetAPI


class NeRFSynthetic(PIDataset):
    """
    PRIVATE CLASS
    - This class and its subclasses are only used inside datasets package.
    """

    def __init__(self, dataset_path: str, dataset_type: typing.Literal['train', 'val', 'test'], downscale: int, use_fp16: bool, use_image_mask: bool):
        super().__init__()
        with open(os.path.join(dataset_path, 'transforms_' + dataset_type + '.json'), 'r') as f:
            transform = json.load(f)
            images = []
            poses = []
            with rich.progress.Progress() as progress:
                task = progress.add_task(f"[cyan]Loading Images ({dataset_type})...", total=len(transform['frames']))
                for frame in transform['frames']:
                    frame_path = os.path.join(dataset_path, frame['file_path'] + '.png')
                    image = torchvision.io.read_image(path=str(frame_path)).permute(1, 2, 0) / 255.0  # (H, W, C)
                    images.append(image)
                    pose = torch.tensor(frame['transform_matrix'])
                    poses.append(pose)
                    progress.update(task, advance=1)
            images = torch.stack(images, dim=0)
            poses = torch.stack(poses, dim=0)
            N, H, W, C = images.shape
            if downscale != 1:
                H, W = H // downscale, W // downscale
                images = torch.nn.functional.interpolate(images.permute(0, 3, 1, 2), size=(H, W), mode='bilinear', align_corners=False).permute(0, 2, 3, 1)
            focal = W / (2 * torch.tan(torch.tensor(transform['camera_angle_x']) / 2))

        self._images = images.to(dtype=torch.float16 if use_fp16 else torch.float32)
        self._poses = poses.to(dtype=torch.float16 if use_fp16 else torch.float32)
        self._focal = focal.to(dtype=torch.float16 if use_fp16 else torch.float32)

        self._near = 0.1
        self._far = 5.0

        self._use_image_mask = use_image_mask

    @property
    def images(self):
        return self._images

    @property
    def images_highlighted(self):
        return None

    @property
    def images_masks(self):
        return self.images[..., 3] > 0

    @property
    def poses(self):
        return self._poses

    @property
    def focal(self):
        return self._focal

    @property
    def width(self):
        return self.images.shape[-2]

    @property
    def height(self):
        return self.images.shape[-3]

    @property
    def near(self):
        return self._near

    @property
    def far(self):
        return self._far

    @property
    def num_poses(self):
        return self.poses.shape[0]

    @property
    def num_times(self):
        return 1

    def transform(self, translate, scale):
        self._poses[:, :3, 3] = (self._poses[:, :3, 3] + torch.as_tensor(translate, dtype=self._poses.dtype, device=self._poses.device).view(1, 3)) * scale
        self._near = self._near * scale
        self._far = self._far * scale

    def __getitem__(self, index):
        return {
            'image': self.images[index],
            'pose': self.poses[index],
            'focal': self.focal,
            'index': index,
            'min_near': self.near,
            'max_far': self.far,
        }

    def __len__(self):
        return len(self.images)


class NeRFSyntheticDataset(PIDatasetAPI):
    """
    BATCH DATA FORMAT:
        images: (N, H, W, C)
        images_masks: (N, H, W)
        poses: (N, 4, 4)
        focals: (N)
        pose_indices: (N)
        min_nears: (N)
        max_fars: (N)
    PUBLIC API:
        dataset_path: str
        aabb_std: list[min_x, min_y, min_z, max_x, max_y, max_z]
        bound_std: list[min_x, min_y, min_z, max_x, max_y, max_z]
        background_color: list[r, g, b]
        complex_background: bool
        num_train_poses: int
    """

    @dataclasses.dataclass
    class Config:
        base_data_dir: str = dataclasses.field(default='data/nerf_synthetic/', metadata={'help': 'base data directory'})
        dataset: typing.Literal['chair', 'drums', 'ficus', 'hotdog', 'lego', 'materials', 'mic', 'ship'] = dataclasses.field(default='lego', metadata={'help': 'dataset name'})
        downscale: int = dataclasses.field(default=1, metadata={'help': 'downscale factor for the dataset images'})
        downscale_val: int = dataclasses.field(default=2, metadata={'help': 'downscale factor for the validation images'})
        fp16: bool = dataclasses.field(default=True, metadata={'help': 'use mixed precision training'})

        pre_translate: list[float] = dataclasses.field(default_factory=lambda: [0.0, 0.0, 0.0], metadata={'help': 'translation to apply to the dataset poses'})
        pre_scale: float = dataclasses.field(default=0.7, metadata={'help': 'scale to apply to the dataset poses'})
        aabb_std: list[float] = dataclasses.field(default_factory=lambda: [-1.0, -1.0, -1.0, 1.0, 1.0, 1.0], metadata={'help': 'standard axis-aligned bounding box for the dataset'})
        bound_std: list[float] = dataclasses.field(default_factory=lambda: [-1.0, -1.0, -1.0, 1.0, 1.0, 1.0], metadata={'help': 'standard bounding box for the dataset'})

    def __init__(self, cfg: Config):
        super().__init__(cfg=cfg)

    def prepare_data(self):
        from huggingface_hub import snapshot_download
        snapshot_download(
            repo_id="XayahHina/nerf_synthetic",
            repo_type="dataset",
            local_dir=self.cfg.base_data_dir,
        )
        if not os.path.exists(os.path.join(self.cfg.base_data_dir, "README.txt")):
            import zipfile
            with zipfile.ZipFile(os.path.join(self.cfg.base_data_dir, "nerf_synthetic.zip"), 'r') as zip_ref:
                zip_ref.extractall(self.cfg.base_data_dir)

    def setup(self, stage: str):
        if "lego" in (self.cfg.base_data_dir + self.cfg.dataset).lower():
            self.cfg.bound_std = [-0.68, -1.0, -0.6, 0.68, 1.0, 1.0]
        super().setup(stage)

    def dataset(self, dataset_type: typing.Literal['train', 'val', 'test']) -> PIDataset:
        downscale = self.cfg.downscale_val if dataset_type == 'val' else self.cfg.downscale
        dataset = NeRFSynthetic(dataset_path=self.cfg.base_data_dir + self.cfg.dataset, dataset_type=dataset_type, downscale=downscale, use_fp16=self.cfg.fp16, use_image_mask=self.complex_background)
        dataset.transform(translate=self.pre_translate, scale=self.pre_scale)
        return dataset

    @staticmethod
    def collate(batch: list):
        images = torch.stack([single['image'] for single in batch])
        poses = torch.stack([single['pose'] for single in batch])
        focals = torch.tensor([single['focal'] for single in batch])
        pose_indices = torch.tensor([single['index'] for single in batch])
        min_nears = torch.tensor([single['min_near'] for single in batch]).to(poses.dtype)
        max_fars = torch.tensor([single['max_far'] for single in batch]).to(poses.dtype)

        return {
            'images': images,
            'images_masks': images[..., 3] > 0,
            'poses': poses,
            'focals': focals,
            'pose_indices': pose_indices,
            'min_nears': min_nears,
            'max_fars': max_fars,
        }

    @property
    def pre_translate(self):
        return self.cfg.pre_translate

    @property
    def pre_scale(self):
        return self.cfg.pre_scale

    @property
    def aabb_std(self):
        return self.cfg.aabb_std

    @property
    def bound_std(self):
        return self.cfg.bound_std

    @property
    def background_color(self):
        return [0.0, 0.0, 0.0]  # Hardcoded for NeRFSynthetic, as it does not use complex backgrounds

    @property
    def complex_background(self):
        return False  # Hardcoded for NeRFSynthetic, as it does not use complex backgrounds
