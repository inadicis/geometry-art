from turtle import Turtle

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
        pen.pencolor(1.0, 1.0, 1.0)
        pen.fillcolor(fill_color)
    for i in range(n_iter):
        pen.begin_fill()
        draw_from_polygon(pen, current_pol)
        pen.end_fill()
        if fill:
            fill_color = tuple([c * 0.99 for c in fill_color])
            pen.fillcolor(fill_color)
            print(fill_color)
        current_pol = current_pol.sub_polygon(ratio)
