#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import viwid
import typing as t
import dataclasses


@dataclasses.dataclass
class Color:
    r: float
    g: float
    b: float

    @property
    def a(self):
        return 1.0

    @staticmethod
    def from_string(s: t.Union["Color", str]) -> "Color":
        if isinstance(s, Color):
            return s
        if len(s) == 7:
            r, g, b = s[1:3], s[3:5], s[5:7]
            scale = 255
        elif len(s) == 4:
            r, g, b = s[1], s[2], s[3]
            scale = 15
        else:
            raise ValueError(f"invalid color string '{s}'")
        return Color(int(r, base=16) / scale, int(g, base=16) / scale, int(b, base=16) / scale)


@dataclasses.dataclass
class FullColor:
    rich: Color
    base: Color

    @staticmethod
    def from_string(s: t.Union[Color, "FullColor", str]) -> "FullColor":
        if isinstance(s, FullColor):
            return s
        if isinstance(s, Color):
            return FullColor(s, s)
        sl = s.split(" ")
        if len(sl) == 1:
            a = b = Color.from_string(sl[0])
        else:
            a = Color.from_string(sl[0])
            b = Color.from_string(sl[1])
        return FullColor(a, b)


class Canvas:

    Color = Color
    FullColor = FullColor

    def __init__(self):
        pass

    def fill(self, color: t.Union[Color, FullColor, str], rectangle: t.Optional[viwid.Rectangle] = None) -> None:
        pass

    def text(self, text, rectangle: t.Optional[viwid.Rectangle] = None) -> None:
        pass

    def cursor(self, point: viwid.Point) -> None:
        pass
