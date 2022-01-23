import random
from turtle import Turtle, Pen, Vec2D
from typing import Callable

from polygon import Polygon, RegularPolygon
from interpolation import *


class Tile:
    def __init__(self, polygon: Polygon):
        self.pen = Pen()
        self.pen.hideturtle()
        self.pen.speed(0)
        self.pen.getscreen().delay(0)
        self.polygons = {
            1.0: [polygon]
        }  # memoize for each ratio
        # the list of subpolygons for any ratio starts with the given polygon.

    def draw_main_polygon(self, *args):
        self.draw_polygon(self.polygons[1.0][0], *args)

    def get_subpolygon(self, index: int, ratio: float):
        """
        Searches if the wanted subpolygon is already calculated and saved. Else calculates recursively until the wanted
        subpolygon, saves all on the way and returns the last one.
        :param index: int
        :param ratio: float
        :return: Polygon
        """
        subpolygons = self.polygons.get(ratio)
        if not subpolygons:
            subpolygons = self.polygons[1.0].copy()
            self.polygons[ratio] = subpolygons
        current_index = len(subpolygons) - 1
        if index <= current_index:
            return subpolygons[index]
        for i in range(current_index, index, 1):
            subpolygons.append(subpolygons[i].next_subpolygon(ratio))
        return subpolygons[index]
        # return subpolygons[-1]

    def draw_polygon(self, polygon: Polygon, closed: bool = True, fill: bool = False):
        self.pen.penup()
        self.pen.goto(polygon.points[0])
        self.pen.pendown()
        if fill:
            self.pen.begin_fill()
        for point in polygon.points:
            self.pen.goto(point)
        if closed:
            self.pen.goto(polygon.points[0])
        if fill:
            self.pen.end_fill()

    def draw_spiral(self, n_iter: int, ratio: float,
                    fill_interpolation: Callable[[float], float] = zero,
                    mirror: bool = False,
                    fill_mode: int = 0,
                    invert_colors: bool = True):
        if mirror:
            ratio = 1 - ratio
        subp = self.get_subpolygon(n_iter, ratio)  # memoize all required polygons
        subpolygons = self.polygons.get(ratio)
        for index, polygon in enumerate(subpolygons):
            match fill_mode:
                case 1:
                    fill_ratio = 1.0 - index / n_iter
                case 2:
                    # print(f'current_poly: {polygon.side_lengths()}')
                    # print(f'first poly: {self.polygons[ratio][0].side_lengths()}')
                    fill_ratio = 1.0 - (sum(polygon.side_lengths()) / len(polygon.side_lengths())) / (sum(
                        self.polygons[ratio][0].side_lengths()) / len(self.polygons[ratio][0].side_lengths()))
                    # print(fill_ratio)
                case _:
                    fill_ratio = random.randint(0, 1000) / 1000

            value = fill_interpolation(fill_ratio)
            if invert_colors:
                value = 1 - value
            self.pen.fillcolor((value, value, value))
            self.pen.pencolor(self.pen.fillcolor())
            self.draw_polygon(polygon, fill=bool(fill_mode))
            if index > n_iter:
                break


class Pavement:
    def __init__(self):
        self.tiles_matrix: list[list[Tile]] = []
        # for i in range(dimensions[0]):
        #     self.tiles_matrix.append([Tile(Polygon()) for _ in range(dimensions[1])])

        self.depth = 100

    def draw(self, ratio: float, inverse_every_row: bool = False, inverse_every_col: bool = False):
        current_spiral_orientation = False
        for row_nr, tile_row in enumerate(self.tiles_matrix):
            for col_nr, tile in enumerate(tile_row):
                tile.draw_spiral(n_iter=self.depth, ratio=ratio, fill_interpolation=gauss_heavy, fill_mode=2,
                                 invert_colors=True, mirror=current_spiral_orientation)
                current_spiral_orientation = not current_spiral_orientation if inverse_every_col else current_spiral_orientation
            current_spiral_orientation = not current_spiral_orientation if inverse_every_row else current_spiral_orientation


class RegularPavement(Pavement):
    def __init__(self, polygon_type: int, polygon_side_length: int,
                 dimensions: (int, int),
                 offsets: ((Vec2D, float), (Vec2D, float)),
                 begin: (Vec2D, float) = (Vec2D(0, 0), 0.0)):
        """

        :param polygon_type: number of sides for the tiles' polygon (either 3,4 or 6 for a filling pavement)
        :param offsets: tuple matrix with 4 elements:
        ((column_change_offset, column_change_rotation), (row_change_offset, row_change_rotation))
        :param polygon_side_length: int
        :param dimensions: tuple, specifying amount of rows and amount of columns
        :param begin: tuple, start point and orientation
        """
        super(RegularPavement, self).__init__()
        current_pos = begin[0]
        current_orientation_angle = begin[1]

        last_row_start_pos = current_pos
        last_row_start_angle = current_orientation_angle

        for row_nr in range(dimensions[0]):
            self.tiles_matrix.append([])
            for col_nr in range(dimensions[1]):
                pol = RegularPolygon(side_length=polygon_side_length, number_of_sides=polygon_type,
                                     first_point=current_pos,
                                     orientation_angle=current_orientation_angle, clockwise=False)
                self.tiles_matrix[row_nr].append(Tile(pol))
                current_pos += offsets[0, 0]
                current_orientation_angle += offsets[0, 1]
            current_pos = last_row_start_pos + offsets[1, 0]
            current_orientation_angle = last_row_start_angle + offsets[1, 1]


class TrianglePavement(RegularPavement):
    def __init__(self, polygon_side_length: int, dimensions: (int, int), begin: (Vec2D, float) = (Vec2D(0, 0), 0.0)):
        sl = polygon_side_length
        col_offsets = (Vec2D(sl, 0.0), 0.0)
        triangle_height = (sl ** 2 - (sl / 2) ** 2) ** 0.5
        row_offsets = (Vec2D(0.5 * sl, triangle_height), math.pi)  # will produce an empty row when trying > 2 rows
        offsets = (col_offsets, row_offsets)

        super().__init__(polygon_type=3, polygon_side_length=polygon_side_length, dimensions=dimensions,
                         offsets=offsets)


class SquarePavement(Pavement):

    def __init__(self, rows: int, columns: int, side_length: int, begin_point: Vec2D = Vec2D(0, 0)):
        super(SquarePavement, self).__init__()
        current_pos = begin_point
        for row_nr in range(rows):
            self.tiles_matrix.append([])
            for col_nr in range(columns):
                pol = RegularPolygon(side_length=side_length, number_of_sides=4, first_point=current_pos,
                                     orientation_angle=0.0, clockwise=False)
                self.tiles_matrix[row_nr].append(Tile(pol))
                current_pos += Vec2D(side_length, 0)
            current_pos = Vec2D(0.0, current_pos[1] + side_length)
