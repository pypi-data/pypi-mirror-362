#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import typing as t


class Size:

    def __init__(self, width: int, height: int):
        self.__width = width
        self.__height = height

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    def extend_by(self, width: int = 0, height: int = 0) -> "Size":
        return Size(self.__width+width, self.__height+height)

    def with_width(self, width: int) -> "Size":
        return Size(width, self.__height)

    def with_height(self, height: int) -> "Size":
        return Size(self.__width, height)


class Point:

    def __eq__(self, o: object) -> bool:
        return isinstance(o, Point) and (self.x == o.x) and (self.y == o.y)

    def __hash__(self) -> int:
        return self.x - self.y

    def __init__(self, x: int, y: int):
        self.__x = x
        self.__y = y

    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    def moved_by(self, x: int = 0, y: int = 0) -> "Point":
        return Point(self.__x+x, self.__y+y)

    def with_x(self, x: int) -> "Point":
        return Point(x, self.__x)

    def with_y(self, y: int) -> "Point":
        return Point(self.__y, y)

    def __add__(self, other):
        return self.moved_by(other.x, other.y)

    def __sub__(self, other):
        return self.moved_by(-other.x, -other.y)


class Rectangle:

    def __init__(self, from_point: Point, to: t.Union[Point, Size]):
        if isinstance(to, Size):
            to = from_point.moved_by(to.width, to.height)
        self.__top_left = Point(min(from_point.x, to.x), min(from_point.y, to.y))
        self.__bottom_right = Point(max(from_point.x, to.x), max(from_point.y, to.y))

    @property
    def top_left(self) -> Point:
        return self.__top_left

    @property
    def bottom_right(self) -> Point:
        return self.__bottom_right

    @property
    def left_x(self) -> int:
        return self.__top_left.x

    @property
    def right_x(self) -> int:
        return self.__bottom_right.x

    @property
    def top_y(self) -> int:
        return self.__top_left.y

    @property
    def bottom_y(self) -> int:
        return self.__bottom_right.y

    @property
    def width(self) -> int:
        return self.right_x - self.left_x

    @property
    def height(self) -> int:
        return self.bottom_y - self.top_y
