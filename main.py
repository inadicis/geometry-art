from drawing import draw_from_polygon, draw_recursive_sub_polygons
from polygon import Polygon, RegularPolygon
import turtle


def main():
    window = turtle.Screen()
    pen = turtle.Turtle()
    pen.speed(0)
    square = RegularPolygon(side_length=500, number_of_sides=5, first_point=turtle.Vec2D(-200, -200), flawed=False)
    draw_recursive_sub_polygons(pen, square, 100, 0.1, fill=False, mirror=True)
    # TODO fix bug that fills even if fill=False
    # todo find a good waay to parametize the color with a function
    draw_recursive_sub_polygons(pen, square, 50, -0.05)
    turtle.done()


if __name__ == "__main__":
    main()