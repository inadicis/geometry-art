import random
from turtle import Turtle, Pen
from typing import Callable

from polygon import Polygon
from interpolation import *


class Artist:
    def __init__(self, polygon: Polygon):
        self.pen = Pen()
        self.pen.hideturtle()
        self.pen.speed(0)
        self.pen.getscreen().delay(0)
        self.polygons = {
            1.0: [polygon]
        }  # memoize for each ratio
        # the list of subpolygons for any ratio starts with the given polygon.

    def draw_main_polygon(self, *args):
        self.draw_polygon(self.polygons[1.0][0], *args)

    def get_subpolygon(self, index: int, ratio: float):
        """
        Searches if the wanted subpolygon is already calculated and saved. Else calculates recursively until the wanted
        subpolygon, saves all on the way and returns the last one.
        :param index: int
        :param ratio: float
        :return: Polygon
        """
        subpolygons = self.polygons.get(ratio)
        if not subpolygons:
            subpolygons = self.polygons[1.0].copy()
            self.polygons[ratio] = subpolygons
        current_index = len(subpolygons) - 1
        if index <= current_index:
            return subpolygons[index]
        for i in range(current_index, index, 1):
            subpolygons.append(subpolygons[i].next_subpolygon(ratio))
        return subpolygons[index]
        # return subpolygons[-1]

    def draw_polygon(self, polygon: Polygon, closed: bool = True, fill: bool = False):
        self.pen.penup()
        self.pen.goto(polygon.points[0])
        self.pen.pendown()
        if fill:
            self.pen.begin_fill()
        for point in polygon.points:
            self.pen.goto(point)
        if closed:
            self.pen.goto(polygon.points[0])
        if fill:
            self.pen.end_fill()

    def draw_spiral(self, n_iter: int, ratio: float,
                    fill_interpolation: Callable[[float], float] = zero,
                    mirror: bool = False,
                    fill_mode: int = 0,
                    invert_colors: bool = True):
        if mirror:
            ratio = 1 - ratio
        subp = self.get_subpolygon(n_iter, ratio)  # memoize all required polygons
        subpolygons = self.polygons.get(ratio)
        for index, polygon in enumerate(subpolygons):
            match fill_mode:
                case 1:
                    fill_ratio = index / n_iter
                case 2:
                    # print(f'current_poly: {polygon.side_lengths()}')
                    # print(f'first poly: {self.polygons[ratio][0].side_lengths()}')
                    fill_ratio = 1.0 - (sum(polygon.side_lengths()) / len(polygon.side_lengths())) / (sum(
                        self.polygons[ratio][0].side_lengths()) / len(self.polygons[ratio][0].side_lengths()))
                    # print(fill_ratio)
                case _:
                    fill_ratio = random.randint(0, 1000) / 1000

            value = fill_interpolation(fill_ratio)
            if invert_colors:
                value = 1 - value
            self.pen.fillcolor((value, value, value))
            self.pen.pencolor(self.pen.fillcolor())
            self.draw_polygon(polygon, fill=bool(fill_mode))
            if index > n_iter:
                break
        # fill modi -> think of new ones
        # TODO fix filling for ratios < 0 or > 1
        # TODO be able to give a triple interpolation function ([0:1] -> [0:1]^3)
        # Todo be able to parametrise line color independly and realtive to fill color?
        # TODO make interpolation not dependant on n_iter, but on area of polygon? perimeter? radius?
