from drawing import Artist
from polygon import Polygon, RegularPolygon
import turtle
from interpolation import *


def main():
    window = turtle.Screen()
    square = RegularPolygon(side_length=500, number_of_sides=5, first_point=turtle.Vec2D(-200, -200), flawed=False)
    art = Artist(square)
    art.draw_spiral(100, 0.05, fill=True, fill_interpolation=cubic)
    turtle.done()


if __name__ == "__main__":
    main()
