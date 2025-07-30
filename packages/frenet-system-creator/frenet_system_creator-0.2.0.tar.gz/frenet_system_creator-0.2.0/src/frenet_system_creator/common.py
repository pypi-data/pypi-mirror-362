"""Utility functions shared across the package."""

from typing import Iterable, Tuple
import math

Point2D = Tuple[float, float]


def calc_distance(point1: Point2D, point2: Point2D) -> float:
    """Return Euclidean distance between two 2-D points."""

    return math.hypot(point1[0] - point2[0], point1[1] - point2[1])


def nearest_point(points: Iterable[Point2D], test_point: Point2D) -> int:
    """Return index of the point in ``points`` closest to ``test_point``."""

    nearest_index = min(range(len(points)), key=lambda i: calc_distance(points[i], test_point))
    return nearest_index
