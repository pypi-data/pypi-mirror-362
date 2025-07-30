#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import viwid.widgets.widget
import curses


class Entry(viwid.widgets.widget.Widget):

    def __init__(self, **kwargs):
        kwargs["horizontal_expand_greedily"] = kwargs.get("horizontal_expand_greedily", True)
        super().__init__(**kwargs)
        self.__cursor_position = 0
        self.__hoffset = 0

    @viwid.widgets.widget.Property(default=lambda: "")
    def text(self, v) -> str:
        self.cursor_position = self.cursor_position

    @property
    def cursor_position(self):
        return self.__cursor_position

    @cursor_position.setter
    def cursor_position(self, value):
        value = value or 0
        if value < 0:
            value = 0
        if value > len(self.text):
            value = len(self.text)
        self.__cursor_position = value

        if self.__cursor_position < self.__hoffset:
            self.__hoffset = self.cursor_position
        elif self.__cursor_position >= self.__hoffset + self.size.width:
            self.__hoffset = max(0, self.__cursor_position-self.size.width+1)

        self.request_repaint()

    def compute_width(self, minimal) -> int:
        return 1 if minimal else 10

    def compute_height(self, width: int, minimal) -> int:
        return 1

    @property
    def focusable(self):
        return True

    def paint(self, canvas):
        canvas.text(self.text[self.__hoffset: self.__hoffset+self.size.width])
        canvas.cursor(viwid.Point(self.cursor_position-self.__hoffset, 0))

    def _keyboard_event(self, event):
        if event.key == curses.KEY_LEFT:
            self.cursor_position -= 1
        elif event.key == curses.KEY_RIGHT:
            self.cursor_position += 1
        elif event.key == curses.KEY_BACKSPACE:
            if self.cursor_position > 0:
                self.cursor_position -= 1
                self.text = self.text[:self.__cursor_position] + self.text[self.__cursor_position+1:]
        elif event.key == curses.KEY_HOME:
            self.cursor_position = 0
        elif event.key == curses.KEY_END:
            self.cursor_position = len(self.text)
        elif event.key == curses.KEY_DC:
            if self.cursor_position < len(self.text):
                self.text = self.text[:self.__cursor_position] + self.text[self.__cursor_position+1:]
        elif event.key < 128:
            self.text = self.text[:self.__cursor_position] + chr(event.key) + self.text[self.__cursor_position:]
            self.cursor_position += 1
        else:
            return
        event.stop_propagation()

    @property
    def class_style_name(self):
        return "entry"
