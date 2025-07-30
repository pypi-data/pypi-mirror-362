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
import os
import random
import typing

import rich.progress
import torch
import torchvision
import yaml

from .api import PIDataset, PIDatasetAPI
from .image_mask import process_video_full_mask


class PINeuFlow(PIDataset):
    """
    PRIVATE CLASS
    - This class and its subclasses are only used inside datasets package.
    """

    def __init__(self, dataset_path: str, dataset_type: typing.Literal['train', 'val', 'test'], downscale: int, use_fp16: bool, use_image_mask: bool):
        super().__init__()
        with open(os.path.join(dataset_path, 'scene_info.yaml'), 'r') as f:
            scene_info = yaml.safe_load(f)
            indices = torch.tensor(scene_info[dataset_type + '_indices'])

            # ---------- Load Base Information ----------
            poses = torch.stack([
                torch.tensor(cam["cam_transform"])
                for cam in scene_info["cameras"]
            ])[indices]
            focals = torch.tensor([
                float(cam["focal"]) * float(cam["width"]) / float(cam["aperture"])
                for cam in scene_info["cameras"]
            ])[indices]
            widths = torch.tensor([
                int(cam["width"])
                for cam in scene_info["cameras"]
            ])[indices]
            heights = torch.tensor([
                int(cam["height"])
                for cam in scene_info["cameras"]
            ])[indices]
            # ---------- Load Base Information ----------

            # ---------- Load videos ----------
            images = []
            with rich.progress.Progress() as progress:
                task = progress.add_task(f"[cyan]Loading Videos ({dataset_type})...", total=len(indices))
                for i in indices:
                    video_path = scene_info['videos'][i]
                    full_path = os.path.normpath(os.path.join(dataset_path, video_path))
                    video_tensor = torchvision.io.read_video(full_path, pts_unit='sec')[0].to(torch.float32) / 255.0
                    images.append(video_tensor)
                    progress.update(task, advance=1)
            images = torch.stack(images)
            # ---------- Load videos ----------

            if use_image_mask:
                # ---------- Load videos highlighted ----------
                images_highlighted = []
                with rich.progress.Progress() as progress:
                    task = progress.add_task(f"[cyan]Loading Highlighted Videos ({dataset_type})...", total=len(indices))
                    for i in indices:
                        video_path = scene_info['videos'][i]
                        highlighted_path = os.path.normpath(os.path.join(dataset_path, os.path.splitext(video_path)[0] + '_highlighted' + os.path.splitext(video_path)[1]))
                        if not os.path.exists(highlighted_path):
                            process_video_full_mask(
                                input_path=os.path.normpath(os.path.join(dataset_path, video_path)),
                                background_color=tuple([x * 255.0 for x in scene_info['background_color']]),
                                color_thresh=scene_info['color_thresh'],
                                dilation_pixels=scene_info['dilation_pixels'],
                            )
                        video_tensor = torchvision.io.read_video(highlighted_path, pts_unit='sec')[0].to(torch.float32) / 255.0
                        images_highlighted.append(video_tensor)
                        progress.update(task, advance=1)
                images_highlighted = torch.stack(images_highlighted)
                # ---------- Load videos highlighted ----------

                # ---------- Load videos masks ----------
                images_masks = []
                with rich.progress.Progress() as progress:
                    task = progress.add_task(f"[cyan]Loading Mask Videos ({dataset_type})...", total=len(indices))
                    for i in indices:
                        video_path = scene_info['videos'][i]
                        mask_path = os.path.normpath(os.path.join(dataset_path, os.path.splitext(video_path)[0] + '_mask' + os.path.splitext(video_path)[1]))
                        if not os.path.exists(mask_path):
                            process_video_full_mask(
                                input_path=os.path.normpath(os.path.join(dataset_path, video_path)),
                                background_color=tuple([x * 255.0 for x in scene_info['background_color']]),
                                color_thresh=scene_info['color_thresh'],
                                dilation_pixels=scene_info['dilation_pixels'],
                            )
                        video_tensor = torchvision.io.read_video(mask_path, pts_unit='sec')[0].to(torch.float32) / 255.0
                        images_masks.append(video_tensor)
                        progress.update(task, advance=1)
                images_masks = torch.stack(images_masks)
                # ---------- Load videos masks ----------

            # ---------- Downscale videos ----------
            V, T, H, W, C = images.shape
            if downscale != 1:
                images = images.permute(0, 1, 4, 2, 3).reshape(V * T, C, H, W)  # [V * T, C, H, W]
                if use_image_mask:
                    images_highlighted = images_highlighted.permute(0, 1, 4, 2, 3).reshape(V * T, C, H, W)  # [V * T, C, H, W]
                    images_masks = images_masks.permute(0, 1, 4, 2, 3).reshape(V * T, C, H, W)  # [V * T, C, H, W]
                H, W = H // downscale, W // downscale
                images = torch.nn.functional.interpolate(images, size=(H, W), mode='bilinear', align_corners=False).reshape(V, T, C, H, W).permute(0, 1, 3, 4, 2)  # [V, T, H, W, C]
                if use_image_mask:
                    images_highlighted = torch.nn.functional.interpolate(images_highlighted, size=(H, W), mode='bilinear', align_corners=False).reshape(V, T, C, H, W).permute(0, 1, 3, 4, 2)  # [V, T, H, W, C]
                    images_masks = torch.nn.functional.interpolate(images_masks, size=(H, W), mode='bilinear', align_corners=False).reshape(V, T, C, H, W).permute(0, 1, 3, 4, 2)  # [V, T, H, W, C]
                focals = focals / downscale
            # ---------- Downscale videos ----------

            # ---------- Load videos masks ----------
            images = images.permute(1, 0, 2, 3, 4)  # [T, V, H, W, C]
            if use_image_mask:
                images_highlighted = images_highlighted.permute(1, 0, 2, 3, 4)  # [T, V, H, W, C]
                images_masks = images_masks.permute(1, 0, 2, 3, 4)  # [T, V, H, W, C]
                images_gray = (
                        0.299 * images_masks[..., 0] +
                        0.587 * images_masks[..., 1] +
                        0.114 * images_masks[..., 2]
                )
                self._images_highlighted = images_highlighted
                self._images_masks = images_gray > 0.8
            else:
                self._images_highlighted = images
                self._images_masks = torch.ones_like(images[..., 0], dtype=torch.bool)
            # ---------- Load videos masks ----------

            # ---------- Prepare Data ----------
            self._images = images.to(dtype=torch.float16 if use_fp16 else torch.float32)
            self._poses = poses.to(dtype=torch.float16 if use_fp16 else torch.float32)
            self._focal = focals.to(dtype=torch.float16 if use_fp16 else torch.float32)
            self._width = widths.to(dtype=torch.float16 if use_fp16 else torch.float32)
            self._height = heights.to(dtype=torch.float16 if use_fp16 else torch.float32)

            self._near = float(scene_info['train_space']['near_std'])
            self._far = float(scene_info['train_space']['far_std'])

            self.times = torch.linspace(0, 1, steps=self.num_frames).to(dtype=torch.float16 if use_fp16 else torch.float32)

        self._use_image_mask = use_image_mask

    @property
    def images(self):
        return self._images

    @property
    def images_highlighted(self):
        return self._images_highlighted

    @property
    def images_masks(self):
        return self._images_masks

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
    def num_frames(self):
        return self.images.shape[0]

    @property
    def num_videos(self):
        return self.images.shape[1]

    @property
    def num_poses(self):
        return self.poses.shape[0]

    @property
    def num_times(self):
        return self.num_frames

    def transform(self, translate, scale):
        self._poses[:, :3, 3] = (self._poses[:, :3, 3] + torch.as_tensor(translate, dtype=self._poses.dtype, device=self._poses.device).view(1, 3)) * scale
        self._near = self._near * scale
        self._far = self._far * scale

    def __getitem__(self, index):
        time_shift = 0
        pose_index = random.randint(0, self.num_poses - 1)

        if index == 0 and time_shift <= 0:
            target_image = self.images[index, pose_index]
            target_time = self.times[index]
        elif index == self.images.shape[0] - 1 and time_shift >= 0:
            target_image = self.images[index, pose_index]
            target_time = self.times[index]
        else:
            if time_shift >= 0:
                target_image = (1 - time_shift) * self.images[index, pose_index] + time_shift * self.images[index + 1, pose_index]
                target_time = (1 - time_shift) * self.times[index] + time_shift * self.times[index + 1]
            else:
                target_image = (1 + time_shift) * self.images[index, pose_index] + (-time_shift) * self.images[index - 1, pose_index]
                target_time = (1 + time_shift) * self.times[index] + (-time_shift) * self.times[index - 1]

        return {
            'image': target_image,
            'image_highlighted': self.images_highlighted[index, pose_index],
            'image_mask': self.images_masks[index, pose_index],
            'pose': self.poses[pose_index],
            'focal': self.focal[pose_index],
            'time': target_time,
            'pose_index': pose_index,
            'frame_index': index,
        }

    def __len__(self):
        return len(self.images)


class PINeuFlowDataset(PIDatasetAPI):
    """
    BATCH DATA FORMAT:
        images: (N, H, W, C)
        images_masks: (N, H, W)
        poses: (N, 4, 4)
        focals: (N)
        times: (N)
        pose_indices: (N)
        frame_indices: (N)
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
        base_data_dir: str = dataclasses.field(default='data/pi_neuflow/', metadata={'help': 'base data directory'})
        dataset: typing.Literal['scalar', 'torch', 'torch_avo', 'torch2', 'torch2_avo', 'fireplace', 'sphere', 'game'] = dataclasses.field(default='scalar', metadata={'help': 'dataset name'})
        downscale: int = dataclasses.field(default=1, metadata={'help': 'downscale factor for the dataset images'})
        downscale_val: int = dataclasses.field(default=2, metadata={'help': 'downscale factor for the validation images'})
        fp16: bool = dataclasses.field(default=True, metadata={'help': 'use mixed precision training'})

    def __init__(self, cfg: Config):
        super().__init__(cfg=cfg)

        self._background_color = None
        self._complex_background = None

        self._pre_translate = None
        self._pre_scale = None
        self._aabb_std = None
        self._bound_std = None

    def prepare_data(self):
        from huggingface_hub import snapshot_download
        snapshot_download(
            repo_id="XayahHina/PI-NeuFlow",
            repo_type="dataset",
            local_dir=self.cfg.base_data_dir,
        )

    def setup(self, stage: str):
        with open(os.path.join(self.cfg.base_data_dir, self.cfg.dataset, 'scene_info.yaml'), 'r') as f:
            scene_info = yaml.safe_load(f)
            self._background_color = scene_info['background_color']
            self._complex_background = int(scene_info['complex_background']) > 0

            train_space = scene_info['train_space']
            self._pre_translate = train_space['pre_translate']
            self._pre_scale = train_space['pre_scale']
            aabb_std_min = train_space['aabb_std_min']
            aabb_std_max = train_space['aabb_std_max']
            self._aabb_std = aabb_std_min + aabb_std_max
            self._bound_std = [-1.0, -1.0, -1.0, 1.0, 1.0, 1.0]
        super().setup(stage)

    def dataset(self, dataset_type: typing.Literal['train', 'val', 'test']) -> PIDataset:
        downscale = self.cfg.downscale_val if dataset_type == 'val' else self.cfg.downscale
        dataset = PINeuFlow(dataset_path=self.cfg.base_data_dir + self.cfg.dataset, dataset_type=dataset_type, downscale=downscale, use_fp16=self.cfg.fp16, use_image_mask=not self.complex_background)
        dataset.transform(translate=self.pre_translate, scale=self.pre_scale)
        return dataset

    @staticmethod
    def collate(batch: list):
        images = torch.stack([single['image'] for single in batch])
        images_highlighted = torch.stack([single['image_highlighted'] for single in batch])
        images_masks = torch.stack([single['image_mask'] for single in batch])
        poses = torch.stack([single['pose'] for single in batch])
        focals = torch.stack([single['focal'] for single in batch])
        times = torch.stack([single['time'] for single in batch])
        pose_indices = torch.tensor([single['pose_index'] for single in batch])
        frame_indices = torch.tensor([single['frame_index'] for single in batch])

        return {
            'images': images,
            'images_highlighted': images_highlighted,
            'images_masks': images_masks,
            'poses': poses,
            'focals': focals,
            'times': times,
            'pose_indices': pose_indices,
            'frame_indices': frame_indices,
        }

    @property
    def pre_translate(self):
        return self._pre_translate

    @property
    def pre_scale(self):
        return self._pre_scale

    @property
    def aabb_std(self):
        return self._aabb_std

    @property
    def bound_std(self):
        return self._bound_std

    @property
    def background_color(self):
        return self._background_color

    @property
    def complex_background(self):
        return self._complex_background
