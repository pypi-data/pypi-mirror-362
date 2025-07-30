#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import enum
import functools
import typing as t
import klovve


class Model(klovve.Model):

    @functools.total_ordering
    class Size(enum.Enum):
        TINY = enum.auto()
        SMALL = enum.auto()
        MEDIUM = enum.auto()
        LARGE = enum.auto()
        EXTRA_LARGE = enum.auto()

        def __lt__(self, other):
            if type(self) is type(other):
                return self.value < other.value

    class Orientation(enum.Enum):
        HORIZONTAL = enum.auto()
        VERTICAL = enum.auto()

    size: Size = klovve.Property(default=Size.MEDIUM)

    orientation: Orientation = klovve.Property()

    text: t.Optional[str] = klovve.Property(default=None)


class View(klovve.BaseView[Model]):
    pass
