# SPDX-FileCopyrightText: © 2025 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only
import functools

import klovve.builtin.drivers.gtk
from klovve.builtin.drivers.gtk import Gdk, Gtk


class LocationBar(klovve.builtin.drivers.gtk.ViewMaterialization[klovve.views.LocationBar]):

    def create_native(self):
        location_bar_box = self.new_native(Gtk.Box, self.piece, layout_manager=LocationBar._BoxLayout(),
                                           css_name="klv_location_bar")
        location_bar_box.append(location_bar_inner_box := self.new_native(Gtk.Box))

        self.piece._introspect.observe_list_property(
            klovve.views.LocationBar.segments,
            klovve.builtin.drivers.gtk.ViewMaterialization.MaterializingViewsInGtkBoxObserver,
            (self, location_bar_inner_box, self.__gtk_button_for_segment), owner=self)

        return location_bar_box

    def __gtk_button_for_segment(self, segment):
        gtk_button = self.new_native(Gtk.Button, css_classes=("flat", "klv_location_bar_button"))
        klovve.effect.activate_effect(self.__refresh_segment_button_label, (segment, gtk_button), owner=gtk_button)
        gtk_button.connect("clicked", lambda *_: self.piece._segment_selected(segment))
        return gtk_button

    def __refresh_segment_button_label(self, segment, gtk_button):
        gtk_button.set_label(f"➣ {self.piece.segment_label_func(segment)}")

    class _BoxLayout(Gtk.BoxLayout):

        def do_measure(self, widget, orientation, for_size):
            if orientation == Gtk.Orientation.VERTICAL:
                if child := widget.get_first_child():
                    return child.measure(orientation, for_size)
            return 0, 0, -1, -1

        def do_allocate(self, widget, width, height, baseline):
            if child := widget.get_first_child():
                child_width = child.measure(Gtk.Orientation.HORIZONTAL, -1)[0]
                allocation = Gdk.Rectangle()
                allocation.x = min(0, width - child_width)
                allocation.y = 0
                allocation.width = child_width
                allocation.height = height
                child.size_allocate(allocation, -1)
