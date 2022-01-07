from drawing import draw_from_polygon, draw_recursive_sub_polygons, Artist
from polygon import Polygon, RegularPolygon
import turtle


def main():
    window = turtle.Screen()
    # pen = turtle.Turtle()
    # pen.speed(0)
    # pen.getscreen().delay()
    square = RegularPolygon(side_length=500, number_of_sides=5, first_point=turtle.Vec2D(-200, -200), flawed=False)
    # draw_recursive_sub_polygons(pen, square, 100, 0.1, fill=False, mirror=True)
    art = Artist(square)
    art.draw_spiral(500, 0.05)
    # draw_recursive_sub_polygons(pen, square, 50, -0.05)
    turtle.done()


if __name__ == "__main__":
    main()
