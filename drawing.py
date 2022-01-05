from turtle import Turtle

from polygon import Polygon


def draw_from_polygon(pen: Turtle, polygon: Polygon):
    pen.penup()
    pen.goto(polygon.points[0])
    pen.pendown()
    for point in polygon.points:
        pen.goto(point)

