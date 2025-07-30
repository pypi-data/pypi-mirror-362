#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import viwid.widgets.label


class Button(viwid.widgets.label.Label):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__on_click = []

    @property
    def focusable(self):
        return True

    @property
    def on_click(self):
        return self.__on_click

    def _mouse_click_event(self, event):
        if event.left_button:
            for handler in self.__on_click:
                handler()
            event.stop_propagation()

    def _keyboard_event(self, event):
        if event.key == 10:
            for handler in self.__on_click:
                handler()
            event.stop_propagation()

    @property
    def class_style_name(self):
        return "control"
