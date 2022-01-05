from drawing import draw_from_polygon
from polygon import Polygon, RegularPolygon
import turtle


def main():
    window = turtle.Screen()

    p = Polygon()
    p.add_points(turtle.Vec2D(10,20), turtle.Vec2D(15, 25), turtle.Vec2D(0, 0), turtle.Vec2D(5, 5))
    t = turtle.Turtle()
    draw_from_polygon(t, p)
    rp = RegularPolygon(side_length=100, number_of_sides=4)
    turtle.done()



if __name__ == "__main__":
    main()