#!/usr/bin/python3
# -*- coding:utf-8 -*-

"""
author：yannan1
since：2024-03-22
"""
from typing import List

import cv2 as cv
import numpy as np

from ..common import AbstractTransform

__all__ = [
    "ColorMeasurement",
    "WidthHeigtMeasurement"
]


class ColorMeasurement(AbstractTransform):

    def __init__(self, poly_vertices=None):
        """ColorMeasurement, 颜色测量, 测量

        Args:
            poly_vertices: Polygon vertices, 候选区点集, [], []
        """
        super().__init__(use_gpu=False)
        if poly_vertices is None:
            poly_vertices = []
        self.poly_vertices = np.array(poly_vertices, np.int32)

    def _apply(self, sample):
        if sample.image is None:
            return sample
        image = sample.image

        if self.poly_vertices:
            mask = np.zeros(image.shape[:2], dtype=np.uint8)
            mask = cv.fillPoly(mask, pts=[self.poly_vertices], color=1)

            non_zero_indices = np.nonzero(mask)
            candidate = image[non_zero_indices]
        else:
            candidate = image

        sample.color_measure = {
            "mean": np.mean(candidate),
            "median": np.median(candidate),
            "max": np.max(candidate),
            "min": np.min(candidate),
            "std": np.std(candidate),
        }

        return sample


class WidthHeightMeasurement(AbstractTransform):
    
    def __init__(self, poly_vertices=None):
        """WidthHeightMeasurement, 宽度高度测量, 测量

        Args:
            poly_vertices: Polygon vertices, 候选区点集, [], []
        """
        super().__init__(use_gpu=False)
        if poly_vertices is None:
            poly_vertices = []
        self.poly_vertices = np.array(poly_vertices, np.int32)

    def _apply(self, sample):
        if sample.image is None:
            return sample
        if self.poly_vertices.size > 0:           
            points = self.poly_vertices.squeeze()  # 将点的坐标转换为 NumPy 数组
            rows = points[:, 1] # 提取所有点的 Y 坐标（行号）
            cols = points[:, 0] # 提取所有点的 X 坐标（列号）
            # 初始化最宽和最窄的宽度,以及最高和最低的高度
            min_width = float('inf')
            max_width = 0
            min_height = float('inf')
            max_height = 0
            
            # 遍历每一行
            for y in np.unique(rows):
                # 获取当前行的所有 X 坐标
                x_coords = cols[rows == y]
                
                # 如果当前行没有点，跳过
                if len(x_coords) == 0:
                    continue
                
                # 当前行的最小和最大 X 坐标
                x_min = np.min(x_coords)
                x_max = np.max(x_coords)
                
                # 当前行的宽度
                width = x_max - x_min + 1  # 加 1 是因为像素本身也要算进去
                
                # 更新最宽和最窄的宽度
                min_width = min(min_width, width)
                max_width = max(max_width, width)
                
            # 遍历每一列
            for x in np.unique(cols):
                # 获取当前列的所有 Y 坐标
                y_coords = rows[cols == x]
                
                # 如果当前行没有点，跳过
                if len(y_coords) == 0:
                    continue
                
                # 当前行的最小和最大 Y 坐标
                y_min = np.min(y_coords)
                y_max = np.max(y_coords)
                
                # 当前列的高度
                height = y_max - y_min + 1  # 加 1 是因为像素本身也要算进去
                
                # 更新最低和最高的高度
                min_height = min(min_height, height)
                max_height = max(max_height, height)

        else:
            min_width = max_width = min_height = max_height = 0


        sample.width_height_measure = {
            "min_width": min_width,
            "max_width": max_width,
            "diff_width": max_width - min_width,
            "min_height": min_height,
            "max_height": max_height,
            "diff_height": max_height - min_height
        }

        return sample



