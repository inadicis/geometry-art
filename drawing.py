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
                    fill: bool = False,
                    invert_colors: bool = True):
        if mirror:
            ratio = 1 - ratio
        subp = self.get_subpolygon(n_iter, ratio)  # memoize all required polygons
        subpolygons = self.polygons.get(ratio)
        for index, polygon in enumerate(subpolygons):
            value = fill_interpolation(index / n_iter)
            if invert_colors:
                value = 1 - value
            self.pen.fillcolor((value, value, value))
            self.pen.pencolor(self.pen.fillcolor())
            self.draw_polygon(polygon, fill=fill)
            if index > n_iter:
                break
        # TODO be able to give a triple interpolation funciton ([0:1] -> [0:1]^3)
        # Todo be able to parametrise line color independly and realtive to fill color?
        # TODO make interpolation not dependant on n_iter, but on area of polygon? perimeter? radius?
