#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import unicodedata

import viwid.widgets.widget


class Label(viwid.widgets.widget.Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @viwid.widgets.widget.Property(default=lambda: "")
    def text(self, value: str):
        self.request_resize()

    def compute_width(self, minimal) -> int:
        if minimal:
            return 1
        return max([len(x) for x in self.text.split("\n")])

    def compute_height(self, width: int, minimal) -> int:
        return len([c for c in self._text_in_width(width) if c == "\n"]) + 1

    @staticmethod
    def __find_last_whitespace(text, i_from, i_to):
        for i in reversed(range(i_from, i_to)):
            c = text[i]
            if unicodedata.category(c) == "Zs":
                return i
        return -1

    def _text_in_width(self, width):
        if width <= 0:
            return self.text
        remaining_text = self.text
        result = ""
        while remaining_text:
            if len(remaining_text) <= width:
                result += remaining_text
                break
            next_linebreak_index = remaining_text.find("\n")
            if -1 < next_linebreak_index <= width:
                result += remaining_text[:next_linebreak_index+1]
                remaining_text = remaining_text[next_linebreak_index+1:]
            else:
                linebreak_whitespace_index = self.__find_last_whitespace(remaining_text, 0, width+1)
                if linebreak_whitespace_index > -1:
                    result += remaining_text[:linebreak_whitespace_index]
                    remaining_text = remaining_text[linebreak_whitespace_index+1:]
                else:
                    result += remaining_text[:width]
                    remaining_text = remaining_text[width:]
                result += "\n"
        return result

    def paint(self, canvas):
        canvas.text(self._text_in_width(self.size.width))
