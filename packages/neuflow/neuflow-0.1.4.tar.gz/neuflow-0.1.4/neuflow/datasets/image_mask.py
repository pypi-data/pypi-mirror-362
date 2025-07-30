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

import cv2
import numpy as np
import rich


def extract_full_foreground_mask(frame, bg_color, color_thresh, dilation_pixels):
    """
    从指定颜色背景图中提取最大前景区域（物体+流体），返回红色叠加图和二值mask（只保留最大连通域）

    参数：
    - frame: 输入图像，np.uint8, shape=(H, W, 3)
    - bg_color: 背景颜色 (R, G, B)
    - color_thresh: 与背景色的欧氏距离阈值
    - dilation_pixels: mask膨胀范围（像素）
    """
    # 1. 计算与背景颜色的距离
    diff = frame.astype(np.int16) - np.array(bg_color, dtype=np.int16)[None, None, :]
    dist = np.linalg.norm(diff, axis=2).astype(np.uint8)

    # 2. 阈值处理得到初始前景
    _, binary = cv2.threshold(dist, color_thresh, 255, cv2.THRESH_BINARY)

    # 3. 膨胀操作
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * dilation_pixels + 1, 2 * dilation_pixels + 1))
    dilated_mask = cv2.dilate(binary, kernel)

    # 4. 连通域分析：只保留最大区域
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(dilated_mask, connectivity=8)

    # 找到最大区域（跳过背景 label=0）
    max_label = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])

    # 构造 mask，仅保留最大连通域
    largest_mask = np.zeros_like(dilated_mask)
    largest_mask[labels == max_label] = 255

    # 5. 红色高亮叠加
    alpha_mask = (largest_mask / 255.0)[..., None]
    red = np.full_like(frame, (0, 0, 255), dtype=np.uint8)
    blended = frame.astype(np.float32) * (1 - 0.4 * alpha_mask) + red.astype(np.float32) * (0.4 * alpha_mask)
    blended = blended.astype(np.uint8)

    return blended, largest_mask


def process_video_full_mask(input_path, background_color, color_thresh=20, dilation_pixels=8):
    cap = cv2.VideoCapture(input_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # 输出路径
    dirname, basename = os.path.split(input_path)
    name, ext = os.path.splitext(basename)
    out_color_path = os.path.join(dirname, f"{name}_highlighted{ext}")
    out_mask_path = os.path.join(dirname, f"{name}_mask{ext}")

    out_color = cv2.VideoWriter(out_color_path, fourcc, fps, (width, height))
    out_mask = cv2.VideoWriter(out_mask_path, fourcc, fps, (width, height), isColor=False)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        highlighted, binary_mask = extract_full_foreground_mask(frame=frame, bg_color=background_color, color_thresh=color_thresh, dilation_pixels=dilation_pixels)

        out_color.write(highlighted)
        out_mask.write(binary_mask)

    cap.release()
    out_color.release()
    out_mask.release()
    rich.print(f"[bold green]Processed video:[/bold green] {input_path}")


if __name__ == "__main__":
    for video in ['train00.mp4', 'train01.mp4', 'train02.mp4', 'train03.mp4', 'train04.mp4']:
        process_video_full_mask(
            input_path="../../data/pi_neuflow/scalar/" + video,
            background_color=(0, 0, 0),  # 黑色背景
            color_thresh=50,  # 与黑色背景的距离阈值
            dilation_pixels=30,  # 膨胀范围
        )
    for video in ['train00.mp4', 'train01.mp4', 'train02.mp4', 'train03.mp4', 'train04.mp4']:
        process_video_full_mask(
            input_path="../../data/pi_neuflow/sphere/" + video,
            background_color=(255, 255, 255),  # 白色背景
            color_thresh=20,  # 与白色背景的距离阈值
            dilation_pixels=8,  # 膨胀范围
        )
    for video in ['train00.mp4', 'train01.mp4', 'train02.mp4', 'train03.mp4', 'train04.mp4', 'train05.mp4', 'train06.mp4']:
        process_video_full_mask(
            input_path="../../data/pi_neuflow/game/" + video,
            background_color=(0, 0, 0),  # 黑色背景
            color_thresh=20,  # 与黑色背景的距离阈值
            dilation_pixels=20,  # 膨胀范围
        )
    for video in ['Torch Simple cam1.mp4', 'Torch Simple cam2.mp4', 'Torch Simple cam3.mp4', 'Torch Simple cam4.mp4', 'Torch Simple cam5.mp4']:
        process_video_full_mask(
            input_path="../../data/pi_neuflow/torch/" + video,
            background_color=(0, 0, 0),  # 黑色背景
            color_thresh=20,  # 与黑色背景的距离阈值
            dilation_pixels=20,  # 膨胀范围
        )
