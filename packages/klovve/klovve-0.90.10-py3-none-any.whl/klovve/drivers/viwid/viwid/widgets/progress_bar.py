#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import viwid.widgets.label
import viwid.widgets.widget


class ProgressBar(viwid.widgets.label.Label):

    def __init__(self, **kwargs):
        super().__init__(horizontal_alignment=viwid.widgets.widget.Alignment.FILL,
                         **kwargs)

    @viwid.widgets.widget.Property(default=lambda: 0)
    def value(self, value):
        self.request_repaint()

    def compute_width(self, minimal):
        return 1 if minimal else 10

    def compute_height(self, width, minimal):
        return 1

    def paint(self, canvas):
        canvas.fill(self.style_atom_by_name("progress_done").background,
                    viwid.Rectangle(viwid.Point(0, 0),
                                    viwid.Point(int(self.value * self.size.width), self.size.height)))

    @property
    def class_style_name(self):
        return "progress_not_done"
