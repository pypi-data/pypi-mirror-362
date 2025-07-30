#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import sys

import viwid.widgets.box
import viwid.widgets.widget

import curses


class Scrollable(viwid.widgets.box.Box):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.vertical_expand_greedily = True
        self.horizontal_expand_greedily = True

    @viwid.widgets.widget.Property()
    def item(self, v):
        self.children = [v] if v else []
        self.set_offset(viwid.Point(0,0))

    @viwid.widgets.widget.Property(default=lambda: True)
    def vertically_scrollable(self, v):
        self.request_resize()

    @viwid.widgets.widget.Property(default=lambda: False)
    def horizontally_scrollable(self, v):
        self.request_resize()

    @property
    def focusable(self):
        return True

    def _preview_keyboard_event(self, event):
        if event.key == curses.KEY_UP:
            self.__move_offset(0, 1)
        elif event.key == curses.KEY_DOWN:
            self.__move_offset(0, -1)
        elif event.key == curses.KEY_LEFT:
            self.__move_offset(1, 0)
        elif event.key == curses.KEY_RIGHT:
            self.__move_offset(-1, 0)
        else:
            return
        event.stop_propagation() # TODO broken?!

    def __move_offset(self, x, y):
        self.set_offset(self.offset.moved_by(x, y))
        if not self.item:
            return
        ox , oy = self.offset.x, self.offset.y
        ax = -max(0, self.inner_size.width - self.size.width)
        ay = -max(0, self.inner_size.height - self.size.height)
        ox = max(min(0, ox), ax)
        oy = max(min(0, oy), ay)
        self.set_offset(viwid.Point(ox, oy))

    def compute_width(self, minimal):
        if minimal:
            return 1
        return super().compute_width(minimal)

    def compute_height(self, width, minimal):
        if minimal:
            return 1
        return super().compute_height(width, minimal)

    def _preview_scroll_event(self, event):
        self.__move_offset(0, event.direction)
        event.stop_propagation()#TODO broken

    def __correct_offset(self):
        if not self.item:
            return
        ox , oy = self.offset.x, self.offset.y
        ax = -max(0, self.inner_size.width - self.size.width)
        ay = -max(0, self.inner_size.height - self.size.height)
        ox = max(min(0, ox), ax)
        oy = max(min(0, oy), ay)
        self.set_offset(viwid.Point(ox, oy))

    def set_size(self, v):
        super().set_size(v, setinner=False)
        if self.item:
            iw = self.item.compute_width(minimal=False) if self.horizontally_scrollable else v.width
            ih = self.item.compute_height(iw, minimal=False) if self.vertically_scrollable else v.height
            self.set_inner_size(viwid.Size(iw, ih))
            self.__move_offset(0, 0)
