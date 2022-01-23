"""
Static methods that all take a float parameter meant to be between 0 and 1 (but can be any), and return a float between
0 and 1. Meant to be used as fill color value in order to have custom shadings. Some return a list of 3 floats
for rgb values.
"""
import math
from typing import Callable

from scipy.stats import norm


# import numpy as np


def _clamp(x: float, lower_limit: float = 0.0, upper_limit: float = 1.0) -> float:
    if x > upper_limit:
        return upper_limit
    if x < lower_limit:
        return lower_limit
    return x


def zero(ratio: float) -> float:
    return 0.0


def _power(exponent: float) -> Callable[[float], float]:
    return lambda x: _clamp(x ** exponent)


def identity(ratio: float) -> float:
    return _power(1.0)(ratio)


def square(ratio: float) -> float:
    return _power(2)(ratio)


def cube(ratio: float) -> float:
    return _power(3)(ratio)


def sinus(ratio: float) -> float:
    return _clamp(math.sin(2 * ratio / math.pi))


def _gauss(mean: float = 0.5, sd: float = 0.3) -> Callable[[float], float]:
    return lambda x: norm.cdf(x, mean, sd)


def gauss(ratio: float) -> float:
    return _gauss()(ratio)


def gauss_heavy(ratio: float) -> float:
    return _gauss(0.8, 0.4)(ratio)


def _logistic_curve(midpoint: float = 0.5, steepness: float = 1.0, max_value: float = 1.0) -> Callable[[float], float]:
    return lambda x: max_value / (1 + math.e ** (-steepness * (x - midpoint)))


def logistic_curve(ratio: float) -> float:
    return _logistic_curve(0.5, 5.0, 1.0)(ratio)


def smooth_step(ratio: float, edge_1: float = 0.0, edge_2: float = 1.0) -> float:
    x = _clamp((ratio - edge_1) / (edge_2 - edge_1))
    return x * x * (3 - 2 * x)


def smoother_step(ratio: float, edge_1: float = 0.0, edge_2: float = 1.0) -> float:
    x = _clamp((ratio - edge_1) / (edge_2 - edge_1))
    return x * x * x * (x * (x * 6 - 15) + 10)


def general_smooth_step(N, x):
    x = _clamp(x, 0.0, 1.0)
    result = 0

    for i in range(N):
        result += pascal_triangle(-N - 1, i) * pascal_triangle(2 * N + 1, N - i) * math.pow(x, N + i + 1)
    return result


def pascal_triangle(a, b):
    result = 1
    for i in range(b):
        result *= (a - i) / (i + 1)
    return result
