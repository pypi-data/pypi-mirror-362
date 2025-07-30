#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import sys

import viwid.widgets.box
import viwid.widgets.widget


class Frame(viwid.widgets.box.Box):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.vertical_expand_greedily = True
        self.horizontal_expand_greedily = True

    @viwid.widgets.widget.Property()
    def item(self, v):
        self.children = [v] if v else []
        self.set_offset(viwid.Point(1, 1))

    def compute_width(self, minimal):
        return super().compute_width(minimal) + 2

    def compute_height(self, width, minimal):
        return super().compute_height(width, minimal) + 2

    def set_size(self, v):
        super().set_size(v, setinner=False)
        if self.item:
            self.set_inner_size(viwid.Size(max(0, v.width-2), max(0, v.height-2)))

    def paint(self, canvas):
        super().paint(canvas)
        self.set_offset(viwid.Point(0, 0))
        #canvas.text("+")  # TODO
        self.set_offset(viwid.Point(1, 1))
