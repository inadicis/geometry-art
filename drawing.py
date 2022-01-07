from turtle import Turtle
from typing import Callable

from polygon import Polygon


def draw_from_polygon(pen: Turtle, polygon: Polygon, fill: bool = True):
    pen.penup()
    pen.goto(polygon.points[0])
    pen.pendown()
    for point in polygon.points:
        pen.goto(point)
    if fill:
        pen.goto(polygon.points[0])


def draw_recursive_sub_polygons(pen: Turtle, main_polygon: Polygon, n_iter: int, ratio: float = 0.5,
                                mirror: bool = False, fill: bool = False):
    """

    :param pen: a Turtle pen to be used
    :param main_polygon: The first polygon that will be drawn. All other will either be within this one or outside (see ratio)
    :param n_iter: the number of polygons to draw
    :param ratio: float, used to calculate the position of the inscribed polygon's points, using linear interpolation
    between successive points. If negative, it will draw always bigger polygons instead of always tinier
    :param mirror: Used to reverse the direction of the recursive polygons
    """
    current_pol = main_polygon
    if mirror:
        ratio = 1 - ratio
    fill_color = (1.0, 1.0, 1.0)
    if fill:
        pen.pencolor(fill_color)
        pen.fillcolor(fill_color)
    for i in range(n_iter):
        if fill:
            pen.begin_fill()
        draw_from_polygon(pen, current_pol)
        if fill:
            pen.end_fill()
            fill_color = tuple([c * 0.99 for c in fill_color])
            # dark_color = tuple([1.0 - c for c in fill_color])
            pen.color(fill_color)
            # print(fill_color)
        current_pol = current_pol.next_subpolygon(ratio)


class Artist:
    def __init__(self, polygon: Polygon):
        self.pen = Turtle()
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
        subpolygons = self.polygons.get(ratio, self.polygons[1.0].copy())
        current_index = len(subpolygons) - 1
        if index <= current_index:
            return subpolygons[index]
        for i in range(current_index, index - 1, step=1):
            subpolygons.append(subpolygons[i].next_subpolygon(ratio))

        return subpolygons[index]
        # return subpolygons[-1]

    def draw_polygon(self, polygon: Polygon, closed: bool = True):
        self.pen.penup()
        self.pen.goto(polygon.points[0])
        self.pen.pendown()
        for point in polygon.points:
            self.pen.goto(point)
        if closed:
            self.pen.goto(polygon.points[0])

    def draw_spiral(self, n_iter: int, ratio: float, fill_interpolation: Callable[[float], float], mirror: bool = False,
                    fill: bool = False):
        """
        :param n_iter:
        :param ratio:
        :param fill_interpolation:
        :param mirror:
        :param fill:
        :return:
        """
        if mirror:
            ratio = 1 - ratio
        subpolygons = self.polygons.get(ratio, self.polygons[1.0].copy())
        self.get_subpolygon(n_iter, ratio)  # memoize all required polygons
        for index, polygon in enumerate(subpolygons):
            self.draw_polygon(polygon)
            if index > n_iter:
                break
        # TODO be able to give any custom interpolation function ([0:1] -> [0:1])
        # TODO be able to give a triple interpolation funciton ([0:1] -> [0:1]^3)
