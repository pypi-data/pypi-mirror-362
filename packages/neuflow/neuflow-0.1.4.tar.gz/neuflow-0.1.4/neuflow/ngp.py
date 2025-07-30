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
import glob
import os
import subprocess
import tempfile
import textwrap

import lightning
import numpy as np
import rich
import rich.progress
import torch
import torchmetrics
import torchvision.utils

from .datasets import PIDatasetAPI, NeRFSyntheticDataset
from .models import NGPModel
from .plugins import PluginLoss
from .renderers import NGPRenderer


class NGPTrainer(lightning.LightningModule):
    @dataclasses.dataclass
    class NGP:
        dataset: NeRFSyntheticDataset.Config = dataclasses.field(default_factory=NeRFSyntheticDataset.Config, metadata={'help': 'NeRF synthetic dataset configuration'})
        model: NGPModel.Config = dataclasses.field(default_factory=NGPModel.Config, metadata={'help': 'model configuration'})
        renderer: NGPRenderer.Config = dataclasses.field(default_factory=NGPRenderer.Config, metadata={'help': 'renderer configuration'})

        # general settings
        gpu_id: int = dataclasses.field(default=0, metadata={'help': 'GPU ID to use for training'})
        gui: bool = dataclasses.field(default=False, metadata={'help': 'whether to use GUI for rendering'})
        ckpt: bool = dataclasses.field(default=False, metadata={'help': 'checkpoint path to load for testing'})

        # training settings
        epochs: int = dataclasses.field(default=100, metadata={'help': 'number of epochs to train the model'})
        lrate: float = dataclasses.field(default=1e-3, metadata={'help': 'learning rate for the optimizer'})
        val_skip: int = dataclasses.field(default=10, metadata={'help': 'number of epochs to skip for validation'})
        save_val_map: bool = dataclasses.field(default=True, metadata={'help': 'whether to output validation images'})
        export_model_only: bool = dataclasses.field(default=False, metadata={'help': 'whether to export model only'})

        # test settings
        test: bool = dataclasses.field(default=False, metadata={'help': 'test mode, load a checkpoint and test the model'})
        export: bool = dataclasses.field(default=False, metadata={'help': 'whether to export fields'})
        export_houdini: bool = dataclasses.field(default=False, metadata={'help': 'whether to export fields'})
        fields: bool = dataclasses.field(default=True, metadata={'help': 'whether to export fields, defaults to True when export or export_houdini is True'})

    def __init__(self, cfg: NGP):
        super().__init__()
        self.cfg = cfg
        self.save_hyperparameters()
        self.model = NGPModel(cfg=cfg.model)
        self.renderer = NGPRenderer(cfg=cfg.renderer)
        self.psnr = torchmetrics.image.PeakSignalNoiseRatio(data_range=1.0)
        self.ssim = torchmetrics.image.StructuralSimilarityIndexMeasure(data_range=1.0)
        self.lpips = torchmetrics.image.lpip.LearnedPerceptualImagePatchSimilarity(net_type='vgg')

    def on_fit_start(self):
        dataset: PIDatasetAPI = self.trainer.datamodule
        self.renderer.set_render_resolution(width=dataset.width, height=dataset.height)
        rich.print(f"[bold green]>>> [Custom]: Render resolution set to {dataset.width}x{dataset.height} <<<[/bold green]")
        self.renderer.set_min_near_far(min_near=dataset.near_std, max_far=dataset.far_std)
        rich.print(f"[bold green]>>> [Custom]: Near and far std set to {dataset.near_std} and {dataset.far_std} <<<[/bold green]")
        self.renderer.set_aabb_std(dataset.aabb_std)
        rich.print(f"[bold green]>>> [Custom]: AABB std set to {dataset.aabb_std} <<<[/bold green]")
        self.renderer.set_bound_std(dataset.bound_std)
        rich.print(f"[bold green]>>> [Custom]: Bound std set to {dataset.bound_std} <<<[/bold green]")
        self.renderer.set_background_color(dataset.background_color)
        rich.print(f"[bold green]>>> [Custom]: Background color set to {dataset.background_color} <<<[/bold green]")
        self.renderer.to(device=self.device)
        rich.print(f"[bold green]>>> [Custom]: Renderer moved to device {self.device} <<<[/bold green]")

    def on_train_batch_start(self, batch, batch_idx):
        for plugin in self.renderer.plugins:
            plugin.on_iter_start()

    def training_step(self, batch, batch_idx):
        result_maps, pixels, pixels_mask = self.renderer.forward(
            model=self.model,
            poses=batch['poses'],
            focals=batch['focals'],
            images=batch['images'],
            pose_indices=batch.get('pose_indices', None),
            images_masks=batch.get('images_masks', None),
        )

        rgb_map = result_maps['rgb_map']
        img_loss = 10000 * torch.nn.functional.mse_loss(rgb_map, pixels[..., :3])
        self.log("img_loss", img_loss, on_step=True, on_epoch=False, prog_bar=True)
        loss = img_loss

        for plugin_loss in filter(lambda v: isinstance(v, PluginLoss), self.renderer.plugins):
            loss += plugin_loss.weight * plugin_loss.loss
            self.log(f"{plugin_loss.name}", plugin_loss.loss, on_step=True, on_epoch=False, prog_bar=True)

        self.log("loss", loss, on_step=True, on_epoch=False, prog_bar=True)
        return loss

    def on_validation_start(self):
        if self.cfg.save_val_map:
            os.makedirs(os.path.join(self.logger.experiment.dir, 'validation_images'), exist_ok=True)

    def validation_step(self, batch, batch_idx):
        if batch_idx % self.cfg.val_skip != 0:
            return None

        result_maps, pixels, pixels_mask = self.renderer.forward(
            model=self.model,
            poses=batch['poses'],
            focals=batch['focals'],
            images=batch['images'],
            pose_indices=batch.get('pose_indices', None),
            images_masks=batch.get('images_masks', None),
        )

        val_loss = torch.nn.functional.mse_loss(result_maps['rgb_map'], pixels[..., :3])
        self.log("val_loss", val_loss, on_step=False, on_epoch=True, prog_bar=True)
        psnr = self.psnr(result_maps['rgb_map'], pixels[..., :3])
        self.log("val_psnr", psnr, on_step=False, on_epoch=True, prog_bar=True)
        ssim = self.ssim(result_maps['rgb_map'].permute(0, 3, 1, 2), pixels[..., :3].permute(0, 3, 1, 2))  # (N, C, H, W)
        self.log("val_ssim", ssim, on_step=False, on_epoch=True, prog_bar=True)
        lpips = self.lpips(result_maps['rgb_map'].permute(0, 3, 1, 2), pixels[..., :3].permute(0, 3, 1, 2))
        self.log("val_lpips", lpips, on_step=False, on_epoch=True, prog_bar=True)

        if self.cfg.save_val_map:
            final_map = self.generate_map(result_maps, pixels, batch.get('images_highlighted', None), pixels_mask)
            torchvision.utils.save_image(final_map.permute(2, 0, 1), os.path.join(self.logger.experiment.dir, 'validation_images', f'{self.current_epoch}_{batch_idx}.png'))

        return val_loss

    def on_test_start(self):
        os.makedirs(os.path.join(self.logger.experiment.dir, 'test_images'), exist_ok=True)

    def test_step(self, batch, batch_idx):
        result_maps, pixels, pixels_mask = self.renderer.forward(
            model=self.model,
            poses=batch['poses'],
            focals=batch['focals'],
            images=batch.get('images', None),
            pose_indices=batch.get('pose_indices', None),
            images_masks=batch.get('images_masks', None),
        )

        final_map = self.generate_map(result_maps, pixels, batch.get('images_highlighted', None), pixels_mask)

        psnr = self.psnr(result_maps['rgb_map'], pixels[..., :3])
        self.log("test_psnr", psnr, on_step=False, on_epoch=True, prog_bar=True)
        ssim = self.ssim(result_maps['rgb_map'].permute(0, 3, 1, 2), pixels[..., :3].permute(0, 3, 1, 2))  # (N, C, H, W)
        self.log("test_ssim", ssim, on_step=False, on_epoch=True, prog_bar=True)
        lpips = self.lpips(result_maps['rgb_map'].permute(0, 3, 1, 2), pixels[..., :3].permute(0, 3, 1, 2))
        self.log("test_lpips", lpips, on_step=False, on_epoch=True, prog_bar=True)
        torchvision.utils.save_image(final_map.permute(2, 0, 1), os.path.join(self.logger.experiment.dir, 'test_images', f'{batch_idx}.png'))

    def on_test_end(self):
        image_dir = os.path.join(self.logger.experiment.dir, 'test_images')
        video_path = os.path.join(self.logger.experiment.dir, 'test_images', 'test_video.mp4')

        image_paths = sorted(
            glob.glob(os.path.join(image_dir, '*.png')),
            key=lambda x: int(os.path.basename(x).split('_')[-1].split('.')[0])
        )

        frames = []
        for path in image_paths:
            img = torchvision.io.read_image(path)  # (C, H, W), dtype=torch.uint8, range [0,255]
            if img.shape[0] == 1:
                img = img.expand(3, -1, -1)
            frames.append(img.permute(1, 2, 0))  # (H, W, C)

        video_tensor = torch.stack(frames, dim=0)  # (T, H, W, 3)
        torchvision.io.write_video(video_path, video_tensor, fps=24)
        rich.print(f"[bold green]✅ Video saved at[/bold green] [cyan]{video_path}[/cyan] with {len(frames)} frames")

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(params=self.parameters(), lr=self.cfg.lrate, eps=1e-15)
        scheduler = {
            "scheduler": torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.9, patience=10, min_lr=1e-5),
            "monitor": "loss",  # what to monitor for the scheduler
            "interval": "epoch",  # when to step the scheduler
            "frequency": 1,
        }
        return {"optimizer": optimizer, "lr_scheduler": scheduler}

    @staticmethod
    def generate_map(result_maps, pixels, pixels_highlighted, pixels_mask):
        rgb_map_column = torch.cat([rgb for rgb in result_maps['rgb_map']], dim=1)
        acc_map_column = torch.cat([rgb for rgb in result_maps['acc_map']], dim=1) if 'acc_map' in result_maps else None
        depth_map_column = torch.cat([rgb for rgb in result_maps['depth_map']], dim=1) if 'depth_map' in result_maps else None

        pixels_column = torch.cat([pixel for pixel in pixels[..., :3]], dim=1) if pixels is not None else None
        pixels_highlighted_column = torch.cat([pixel for pixel in pixels_highlighted[..., :3]], dim=1) if pixels_highlighted is not None else None
        pixels_mask_column = torch.cat([mask for mask in pixels_mask.unsqueeze(-1)], dim=1) if pixels_mask is not None else None

        final_map = rgb_map_column
        if acc_map_column is not None:
            final_map = torch.cat([final_map, acc_map_column.expand_as(rgb_map_column)], dim=1)
        if depth_map_column is not None:
            final_map = torch.cat([final_map, depth_map_column.expand_as(rgb_map_column)], dim=1)
        if pixels_mask_column is not None:
            final_map = torch.cat([pixels_mask_column.expand_as(rgb_map_column), final_map], dim=1)
        if pixels_highlighted_column is not None:
            final_map = torch.cat([pixels_highlighted_column, final_map], dim=1)
        if pixels_column is not None:
            final_map = torch.cat([pixels_column, final_map], dim=1)

        return final_map

    def export_explicit_fields(self, output_dir, hython_path):
        aabb_std = self.renderer.aabb_std.cpu()  # [low_x, low_y, low_z, high_x, high_y, high_z]
        bound_std = self.renderer.bound_std.cpu()  # [low_x, low_y, low_z, high_x, high_y, high_z]

        weightx = (aabb_std[3] - aabb_std[0]).item() / 2
        weighty = (aabb_std[4] - aabb_std[1]).item() / 2
        weightz = (aabb_std[5] - aabb_std[2]).item() / 2

        min_bound = bound_std[:3]  # [low_x, low_y, low_z]
        max_bound = bound_std[3:]  # [high_x, high_y, high_z]

        resx, resy, resz = int(256 * weightx), int(256 * weighty), int(256 * weightz)
        coords_x = torch.linspace(0, 1, steps=resx + 1)
        centers_x = (coords_x[:-1] + coords_x[1:]) / 2
        coords_y = torch.linspace(0, 1, steps=resy + 1)
        centers_y = (coords_y[:-1] + coords_y[1:]) / 2
        coords_z = torch.linspace(0, 1, steps=resz + 1)
        centers_z = (coords_z[:-1] + coords_z[1:]) / 2
        x, y, z = torch.meshgrid(centers_x, centers_y, centers_z, indexing='ij')
        xyz = torch.stack([x, y, z], dim=-1).view(-1, 3)
        mask_inside = ((xyz >= min_bound) & (xyz <= max_bound)).all(dim=-1)
        xyz = xyz.to(torch.float16 if self.cfg.dataset.fp16 else torch.float32).to(self.device)

        with torch.no_grad():
            with torch.amp.autocast('cuda', enabled=True):
                self.eval()
                with rich.progress.Progress() as progress:
                    task = progress.add_task("[green]Exporting density fields...", total=xyz.shape[0])
                    chunk = 1024 * 8
                    sigma = []
                    for start_idx in range(0, xyz.shape[0], chunk):
                        ret = self.model.sigma(xyz[start_idx:start_idx + chunk])
                        _sigma = ret[0]
                        sigma.append(_sigma.detach().cpu())
                        progress.update(task, advance=(min(start_idx + chunk, xyz.shape[0]) - start_idx))
                    sigma = torch.cat(sigma, dim=0)
                    sigma[~mask_inside] = 0.0
                    sigma = sigma.reshape(resx, resy, resz, 1)

                if hython_path is not None:
                    def execute_template_script(script_content):
                        with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w", encoding="utf-8") as f:
                            temp_script_path = f.name
                            f.write(textwrap.dedent(script_content))
                        try:
                            subprocess.run([hython_path, temp_script_path], check=True)
                        except subprocess.CalledProcessError as e:
                            raise RuntimeError(f"Failed to execute Houdini script: {e}") from e
                        finally:
                            os.remove(temp_script_path)

                    with tempfile.NamedTemporaryFile(suffix=".npy", delete=False) as f:
                        temp_file = f.name
                    np.save(temp_file, sigma.numpy())
                    houdini_code = f'''
                        import hou
                        import numpy as np
                        import os
                        nparray = np.load(r"{temp_file}")
                        resx, resy, resz = nparray.shape[0:3]
                        geo = hou.Geometry()
                        name_attrib = geo.addAttrib(hou.attribType.Prim, "name", "default")
                        vol = geo.createVolume(resx, resy, resz, hou.BoundingBox(0.0, 0.0, 0.0, 1.0, 1.0, 1.0))
                        vol.setAttribValue(name_attrib, "density")
                        vol.setAllVoxels(nparray.flatten().tolist())
                        os.makedirs(r"{output_dir}", exist_ok=True)
                        out_file = os.path.join(r"{output_dir}", f"sigma.bgeo.sc")
                        geo.saveToFile(out_file)
                        '''
                    try:
                        execute_template_script(script_content=houdini_code)
                        gplay_exe = os.path.join(os.path.dirname(hython_path), 'gplay.exe')
                        sigma_file = os.path.join(output_dir, f"sigma.bgeo.sc")
                        rich.print(f"[bold green]Executing[/bold green] [cyan]{gplay_exe} {sigma_file}[/cyan]")
                        subprocess.run([gplay_exe, sigma_file], check=True)
                    except subprocess.CalledProcessError as e:
                        raise RuntimeError(f"Failed to execute Houdini script: {e}") from e
                    finally:
                        os.remove(temp_file)
                else:
                    torch.save(sigma, os.path.join(output_dir, f'sigma.pt'))
                    rich.print(f"[bold green]✅ Density field saved at[/bold green] [cyan]{os.path.join(output_dir, f'sigma.pt')}[/cyan] with shape [magenta]{sigma.shape}[/magenta]")
