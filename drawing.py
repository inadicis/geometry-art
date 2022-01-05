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


def draw_recursive_sub_polygons(pen: Turtle, main_polygon: Polygon, n_iter: int, ratio: float = 0.5):
    current_pol = main_polygon
    for i in range(n_iter):
        draw_from_polygon(pen, current_pol)
        current_pol = current_pol.sub_polygon(ratio)
