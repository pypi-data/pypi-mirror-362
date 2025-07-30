#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import viwid.widgets.button
import viwid.widgets.widget


class CheckButton(viwid.widgets.button.Button):

    @viwid.widgets.widget.Property(default=lambda: False)
    def checked(self, value):
        self.request_repaint()

    def compute_width(self, minimal):
        return super().compute_width(minimal) + 2

    def compute_height(self, width, minimal):
        return super().compute_height(max(0,width-2), minimal)

    def paint(self, canvas):
        symbol = "X" if self.checked else "O"
        canvas.text(symbol + " " + self._text_in_width(self.size.width-2))

    def _keyboard_event(self, event):
        if event.key == 10 or event.key == 32:
            self.checked = not self.checked
            event.stop_propagation()

    def _mouse_click_event(self, event):
        if event.left_button:
            self.checked = not self.checked
            event.stop_propagation()
