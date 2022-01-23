from drawing import Tile
from polygon import Polygon, RegularPolygon  # , Point
import turtle
from interpolation import *


def main():
    window = turtle.Screen()
    pol = RegularPolygon(side_length=100, number_of_sides=5, first_point=turtle.Vec2D(-200, -200), flawed=True)
    art = Tile(pol)
    art.draw_spiral(200, -0.1, fill_mode=0, fill_interpolation=gauss_heavy, invert_colors=True)
    turtle.done()


if __name__ == "__main__":
    main()
