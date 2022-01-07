import turtle
from turtle import Vec2D
import math


def linear_interpolation(a, b, ratio: float):
    return a * ratio + b * (1 - ratio)


class Polygon:

    def __init__(self, ):
        self.points = []  # Vec2D

    def add_points(self, *points: list[Vec2D]):
        for point in points:
            self.points.append(point)

    def next_subpolygon(self, ratio: float) -> 'Polygon':
        subp = Polygon()
        for index, point in enumerate(self.points):
            next_point = self.points[self.next_point_index(index)]
            new_point = linear_interpolation(point, next_point, ratio)
            subp.add_points(new_point)
        return subp

    def next_point_index(self, index: int) -> int:
        return index + 1 if index < len(self.points) - 1 else 0


class RegularPolygon(Polygon):
    def __init__(self,
                 number_of_sides: int,
                 side_length: float,
                 first_point: Vec2D = Vec2D(0, 0),
                 orientation_angle: float = 0.0,
                 clockwise: bool = False,
                 flawed: bool = False):
        """

        :param number_of_sides:
        :param side_length:
        :param first_point: vec2D,
        :param orientation_angle: the angle for the first side in radians. comparing to the vector (1,0)
        :param clockwise: bool, if turning clockwise each angle or not
        """
        super().__init__()
        self.points.append(first_point)
        angle_delta = math.pi - ((number_of_sides - 2) * math.pi / number_of_sides)
        if flawed:
            angle_delta = (number_of_sides - 2) * math.pi / number_of_sides
        for i in range(number_of_sides - 1):
            x_delta = math.cos(orientation_angle) * side_length
            y_delta = math.sin(orientation_angle) * side_length
            self.points.append(Vec2D(self.points[-1][0] + x_delta, self.points[-1][1] + y_delta))

            if clockwise:
                angle_delta *= -1
            orientation_angle += angle_delta
