# SPDX-FileCopyrightText: © 2025 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only
import functools

import viwid.styling

import klovve.builtin.drivers.viwid


class LocationBar(klovve.builtin.drivers.viwid.ViewMaterialization[klovve.views.LocationBar]):

    def create_native(self):
        location_bar_viewport = self.new_native(viwid.widgets.viewport.Viewport, self.piece, class_style="tab_bar",
                                                vertical_alignment=viwid.Alignment.START,
                                                is_horizontally_scrollable=True)
        location_bar_viewport.body = location_bar_box = self.new_native(viwid.widgets.box.Box)
        location_bar_box.children.append(location_bar_inner_box := self.new_native(viwid.widgets.box.Box,
                                                                                   minimal_size=viwid.Size(1, 1)))

        self.piece._introspect.observe_list_property(
            klovve.views.LocationBar.segments,
            klovve.builtin.drivers.viwid.ViewMaterialization.MaterializingViewsInViwidBoxObserver,
            (self, location_bar_inner_box, self.__viwid_button_for_segment), owner=self)
        location_bar_viewport.listen_event(viwid.event.widget.ResizeEvent,
                                           lambda *_: self.__handle_resized(location_bar_viewport))
        location_bar_viewport.listen_event(viwid.widgets.viewport.Viewport.BodyResizedEvent,
                                           lambda *_: self.__handle_resized(location_bar_viewport))
        self.__handle_resized(location_bar_viewport)

        return location_bar_viewport

    def __handle_resized(self, location_bar_viewport: viwid.widgets.viewport.Viewport):
        location_bar_viewport.offset = viwid.Offset(min(
            0, location_bar_viewport.size.width - location_bar_viewport.body.size.width), 0)

    def __viwid_button_for_segment(self, segment):
        default_button_style = viwid.styling.default_theme().main.control  # TODO use correct widget theme
        viwid_button = self.new_native(viwid.widgets.button.Button, margin=viwid.Margin(right=1),
                                       class_style=viwid.styling.Theme.Layer.Class(
                                           normal=viwid.styling.Theme.Layer.Class.Style(foreground="#44F"),
                                           hovered=default_button_style.hovered,
                                           focused=default_button_style.focused,
                                           activated=default_button_style.activated,
                                           disabled=default_button_style.disabled),
                                       decoration=viwid.widgets.button.Decoration.NONE)
        klovve.effect.activate_effect(self.__refresh_segment_button_label, (segment, viwid_button), owner=viwid_button)
        viwid_button.listen_event(viwid.widgets.button.Button.TriggeredEvent,
                                  lambda *_: self.piece._segment_selected(segment))
        return viwid_button

    def __refresh_segment_button_label(self, segment, viwid_button):
        viwid_button.text = f"> {self.piece.segment_label_func(segment)}"
