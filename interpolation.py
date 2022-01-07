"""
Static methods that all take a float parameter meant to be between 0 and 1 (but can be any), and return a float between
0 and 1. Meant to be used as fill color value in order to have custom shadings. Some return a list of 3 floats
for rgb values.
"""
import math
from typing import Callable

from scipy.stats import norm


# import numpy as np


def _crop(ratio: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    if ratio > maximum:
        return maximum
    if ratio < minimum:
        return minimum
    return ratio


def zero(ratio: float) -> float:
    return 0.0


def _power(exponent: float) -> Callable[[float], float]:
    return lambda x: _crop(x ** exponent)


def identity(ratio: float) -> float:
    return _power(1.0)(ratio)


def square(ratio: float) -> float:
    return _power(2)(ratio)


def cube(ratio: float) -> float:
    return _power(3)(ratio)


def sinus(ratio: float) -> float:
    return _crop(math.sin(ratio / math.pi))


def _gauss(mean: float = 0.5, sd: float = 0.3) -> Callable[[float], float]:
    return lambda x: norm.cdf(x, mean, sd)


def gauss(ratio: float) -> float:
    return _gauss()(ratio)


def _logistic_curve(midpoint: float = 0.5, steepness: float = 1.0, max_value: float = 1.0) -> Callable[[float], float]:
    return lambda x: max_value / (1 + math.e ** (-steepness * (x - midpoint)))


def logistic_curve(ratio: float) -> float:
    return _logistic_curve(0.5, 5.0, 1.0)(ratio)
