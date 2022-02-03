import turtle
from turtle import Vec2D
import math

# class Point(Vec2D):
#     def distance(self, other_point):
#         vec = (other_point - self)
#         return (vec[0] ** 2 + vec[1] ** 2) ** 0.5
from typing import List, Tuple


def linear_interpolation(a, b, ratio: float):
    return a * ratio + b * (1 - ratio)


class PolygonBuilder:

    def __init__(self):
        self.vectors_sequence: List[Vec2D] = []  # from first point, "go-to" instructions
        self.instructions_sequence: List[Tuple[float, float]] = []  # length, rotation angle
        self.vectors_star: List[Vec2D]  # position of all points relative to an arbitrarly chosen one
        self.instructions_star: List[Tuple[float, float]] = []  # length, rotation angle


class Polygon:

    def __init__(self, *points: Vec2D):
        self.points: list[Vec2D] = list(points)

    def __eq__(self, other: 'Polygon'):
        """
        Checks that every point are in the same order in both polygons.
        :param other: Polygon
        :return: bool
        """
        # return len(self.points) == len(other.points) and all([p in other.points for p in self.points])
        if len(self.points) != len(other.points):
            return False
        try:
            current_other_index = other.points.index(self.points[0])
        except ValueError:
            return False
        for p in self.points:
            if other.points[current_other_index] != p:
                return False
            current_other_index = other.next_point_index(current_other_index)

    def __reversed__(self):
        return Polygon(*list(reversed(self.points)))

    def add_points(self, *points: Vec2D):
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

    def side_lengths(self):
        lengths = []
        for index, current_point in enumerate(self.points):
            next_point = self.points[self.next_point_index(index)]
            vec = current_point - next_point
            lengths.append((vec[0] ** 2 + vec[1] ** 2) ** 0.5)
        return lengths
        # return [p.distance(self.points[self.next_point_index(index)]) for index, p in enumerate(self.points)]

    def reverse_direction(self):
        self.points = self.points[::-1]

    def area(self):
        pass

    def is_self_intersecting(self):
        pass

    def is_simple(self):
        return not self.is_self_intersecting()

    def centroid(self):
        pass

    def is_star_shaped(self):
        pass

    def adjacent_polygons(self):
        pass

    # def kernel(self):
    #     """set of points that fulfill star-shaped attribute. """


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
        :param first_point: Point,
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
