from drawing import Tile, TrianglePavement
from polygon import Polygon, RegularPolygon  # , Point
import turtle
from interpolation import *


def main():
    window = turtle.Screen()
    # pol = RegularPolygon(side_length=100, number_of_sides=5, first_point=turtle.Vec2D(-200, -200), flawed=True)
    # art = Tile(pol)
    # art.draw_spiral(200, -0.1, fill_mode=0, fill_interpolation=gauss_heavy, invert_colors=True)
    pavement = TrianglePavement(polygon_side_length=300, matrix_dimensions=(20, 20),
                                begin_state=(turtle.Vec2D(-1500, -700), 0.0))
    pavement.draw(ratio=0.01, inverse_every_col=True, inverse_every_row=True)
    turtle.done()


if __name__ == "__main__":
    main()
