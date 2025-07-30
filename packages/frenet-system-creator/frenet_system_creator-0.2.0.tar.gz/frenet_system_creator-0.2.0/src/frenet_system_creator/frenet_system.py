"""Frenet frame conversions and utilities."""

from typing import Iterable, Tuple

import numpy as np
import math
from scipy.interpolate import CubicSpline
from scipy.optimize import minimize_scalar

from .common import calc_distance, nearest_point


class FrenetSystem:
    """Convert between Cartesian and Frenet frames for a 2-D reference path."""

    def __init__(self, vertices: Iterable[Tuple[float, float]]):
        """Initialize the system with a sequence of path vertices."""

        self.vertices = np.array(vertices)
        self.vertices_size = len(self.vertices)
        self.start_vertex = self.vertices[0]
        self.end_vertex = self.vertices[-1]

        # Pre-compute interpolation of x(s) and y(s)
        self.x_values = self.vertices[:, 0]
        self.y_values = self.vertices[:, 1]
        self.s_values = self.generate_s_values()

        self.s_x_interpolator = CubicSpline(self.s_values, self.x_values, bc_type="natural")
        self.s_y_interpolator = CubicSpline(self.s_values, self.y_values, bc_type="natural")

    def generate_s_values(self) -> np.ndarray:
        """Return the accumulated distance ``s`` for each vertex."""

        s_values = [0.0]
        total_distance = 0.0
        for i in range(self.vertices_size - 1):
            current_vertex = self.vertices[i]
            next_vertex = self.vertices[i + 1]
            current_distance = np.linalg.norm(current_vertex - next_vertex)
            total_distance += current_distance
            s_values.append(total_distance)

        return np.array(s_values)

    def get_k_with_s_in_xy(self, s_value: float) -> float:
        """Return derivative dy/dx at the given ``s`` value."""

        dx_divide_ds = self.s_x_interpolator.derivative()(s_value)
        dy_divide_ds = self.s_y_interpolator.derivative()(s_value)
        return dy_divide_ds / dx_divide_ds

    def find_point_r(
        self,
        input_point: Tuple[float, float],
        step: float = 1.0,
        tolerance: float = 1e-4,
        max_iterations: int = 5000,
    ) -> Tuple[np.ndarray, float]:
        """Return the projection of ``input_point`` onto the reference path."""

        nearest_index = nearest_point(self.vertices, input_point)
        s_current = self.s_values[nearest_index]
        step_direction = 1
        best_distance = float("inf")
        current_iterations = 0

        # Function to minimize (distance between the normal line and input_point)
        def distance_function(s):
            x = self.s_x_interpolator(s)
            y = self.s_y_interpolator(s)
            curve_point = np.array([x, y])
            k = self.get_k_with_s_in_xy(s)
            c = -(curve_point[0] + k * curve_point[1])
            a = 1
            b = k
            distance = abs(a * input_point[0] + b * input_point[1] + c) / math.sqrt(a * a + b * b)
            return distance, k

        while best_distance > tolerance and current_iterations < max_iterations:
            s_next = s_current + step_direction * step
            distance_current, _ = distance_function(s_current)
            distance_next, _ = distance_function(s_next)

            if distance_next < distance_current:
                s_current = s_next
                best_distance = distance_next
            else:
                step_direction *= -1
                step /= 2
                best_distance = distance_current

            current_iterations += 1
        x_current = self.s_x_interpolator(s_current)
        y_current = self.s_y_interpolator(s_current)
        return np.array([x_current, y_current]), s_current

    def find_point_r_scalar(
            self,
            input_point: Tuple[float, float],
            s_bounds: Tuple[float, float] = None
    ) -> Tuple[np.ndarray, float]:
        """使用 minimize_scalar 优化 input_point 到曲线上的最近投影点。"""

        def distance_function(s):
            x = self.s_x_interpolator(s)
            y = self.s_y_interpolator(s)
            return np.linalg.norm(np.array([x, y]) - np.array(input_point))

        # 默认全局搜索范围（也可以设为附近一段）
        if s_bounds is None:
            s_bounds = (self.s_values[0], self.s_values[-1])

        result = minimize_scalar(distance_function, bounds=s_bounds, method="bounded")
        s_best = result.x
        x_best = self.s_x_interpolator(s_best)
        y_best = self.s_y_interpolator(s_best)

        return np.array([x_best, y_best]), s_best

    def cartesian2ds_frame(self, input_point: Tuple[float, float]) -> Tuple[np.ndarray, np.ndarray]:
        """Convert a Cartesian point to [d, s] in the Frenet frame."""

        best_point, s = self.find_point_r_scalar(input_point)
        abs_dist = calc_distance(input_point, best_point)
        s_next = s + 0.1
        x0 = self.s_x_interpolator(s)
        y0 = self.s_y_interpolator(s)
        x1 = self.s_x_interpolator(s_next)
        y1 = self.s_y_interpolator(s_next)
        x2, y2 = input_point
        vector1 = np.array([x1 - x0, y1 - y0])
        vector2 = np.array([x2 - x0, y2 - y0])
        sign_of_d = np.sign(np.cross(vector1, vector2))
        d_value = sign_of_d * abs_dist

        return np.array([round(d_value, 7), round(s, 7)]), best_point
    
    def ds_frame2cartesian(self, input_point: Tuple[float, float]) -> np.ndarray:
        """Convert a point expressed in [d, s] back to Cartesian coordinates."""

        d_value, s_value = input_point
        s_next = s_value + 0.1
        x0 = self.s_x_interpolator(s_value)
        y0 = self.s_y_interpolator(s_value)
        x1 = self.s_x_interpolator(s_next)
        y1 = self.s_y_interpolator(s_next)
        vector1 = np.array([x1 - x0, y1 - y0])
        
        # vector1 逆时针旋转 90 度得到法线方向
        vector_norm = np.array([-vector1[1], vector1[0]])
        
        # 将 vector_norm 标准化
        vector_norm = vector_norm / np.linalg.norm(vector_norm)
        
        # 使用 d_value 确定最终的目标点
        # 由于 vector_norm 已经是单位向量，直接乘以 d_value 来得到沿法线方向的偏移
        dx = vector_norm[0] * d_value
        dy = vector_norm[1] * d_value
        
        # 计算并返回最终目标点的坐标
        x_result = x0 + dx
        y_result = y0 + dy
        
        return np.array([x_result, y_result])



