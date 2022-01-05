from drawing import draw_from_polygon, draw_recursive_sub_polygons
from polygon import Polygon, RegularPolygon
import turtle


def main():
    window = turtle.Screen()
    pen = turtle.Turtle()
    pen.speed(0)
    square = RegularPolygon(side_length=500, number_of_sides=3, first_point=turtle.Vec2D(-200, -200))
    draw_recursive_sub_polygons(pen, square, 100, 0.05)
    turtle.done()


if __name__ == "__main__":
    main()