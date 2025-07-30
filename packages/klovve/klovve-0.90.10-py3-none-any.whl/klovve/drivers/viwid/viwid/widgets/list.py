#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import viwid.widgets.box
import viwid.widgets.button
import viwid.widgets.label
import viwid.widgets.widget
import viwid.canvas

import curses


class List(viwid.widgets.box.Box):

    def __init__(self, **kwargs):
        super().__init__(
            orientation=viwid.widgets.box.Orientation.VERTICAL,
            **kwargs)
        self.__items = []
        self.__last_selected_item = None
        self.__on_selection_activated = []

    @property
    def focusable(self):
        return True

    @property
    def on_selection_activated(self):
        return self.__on_selection_activated

    @property
    def items(self):
        return self.children # TODO

    @items.setter
    def items(self, value):
        self.__items = value
        self.children = value

    @viwid.widgets.widget.Property
    def selected_item_index(self, value):
        if self.__last_selected_item is not None:
            self.__last_selected_item.is_selected = False
        if value is not None:
            self.__last_selected_item = self.__items[value]
            self.__items[value].is_selected = True

    @property
    def class_style_name(self):
        return "list"

    def _keyboard_event(self, event):
        if len(self.items) > 0:
            if event.key == curses.KEY_UP:
                if self.selected_item_index is None:
                    self.selected_item_index = 0
                    event.stop_propagation()
                elif self.selected_item_index > 0:
                    self.selected_item_index -= 1
                    event.stop_propagation()
            elif event.key == curses.KEY_DOWN:
                if self.selected_item_index is None:
                    self.selected_item_index = 0
                    event.stop_propagation()
                elif self.selected_item_index < len(self.items)-1:
                    self.selected_item_index += 1
                    event.stop_propagation()
            elif event.key == 10:
                for func in self.__on_selection_activated:
                    func()
                event.stop_propagation()

    def _mouse_click_event(self, event):
        if event.left_button:
            self.try_focus()
            ppx = self.screen.translate_coordinates(event.screen_position, new_origin=self)
            x,y =ppx.x, ppx.y
            row = self.child_at_position(x, y)
            if row:
                try:
                    i = self.__items.index(row)
                except ValueError:
                    i = None
                if i is not None:
                    self.selected_item_index = i
                    for func in self.__on_selection_activated:
                        func()
                    event.stop_propagation()
                    return
        super()._mouse_click_event(event)


class ListRow(viwid.widgets.label.Label):

    def __init__(self, **kwargs):
        super().__init__(
            horizontal_alignment=viwid.widgets.widget.Alignment.FILL,
            **kwargs)

    @viwid.widgets.widget.Property
    def is_selected(self, value):
        self.request_repaint()

    @property
    def class_style_name(self):
        return "selected" if self.is_selected else "list_item"
