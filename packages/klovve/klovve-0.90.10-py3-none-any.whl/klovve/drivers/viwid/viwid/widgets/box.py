#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import enum
import viwid.widgets.widget
import viwid.layout


class Orientation(enum.Enum):
    VERTICAL = enum.auto()
    HORIZONTAL = enum.auto()


class Box(viwid.widgets.widget.Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__orientation = Orientation.VERTICAL
        self.set_layout(viwid.layout.GridLayout(self._partitioning2))

    @property
    def orientation(self):
        return self.__orientation

    @orientation.setter
    def orientation(self, value):
        self.__orientation = value
        self.request_repaint()

    def _partitioning2(self):
        if self.orientation == Orientation.VERTICAL:
            return ((child,) for child in self.children)
        else:
            return (tuple(self.children),)

    def __item_added(self, index: int, item: object) -> None:
        self._children.insert(index, item)

    def __item_removed(self, index: int) -> None:
        self._children.pop(index)

    @viwid.widgets.widget.ListProperty(__item_added, __item_removed)
    def children(self) -> list:
        pass


class CBox(Box):

    @property
    def class_style_name(self):
        return "root"
