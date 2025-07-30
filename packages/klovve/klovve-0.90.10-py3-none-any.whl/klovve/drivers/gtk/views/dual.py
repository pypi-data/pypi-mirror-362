#  SPDX-FileCopyrightText: © 2021 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve.pieces.dual
import klovve.drivers.gtk

Gtk = klovve.drivers.gtk.Gtk


class View(klovve.pieces.dual.View, klovve.drivers.gtk.View):

    def create_native(self):
        pieces, props = self.make_view()

        result = self.gtk_new(Gtk.Box, orientation=Gtk.Orientation.HORIZONTAL)

        inner_left_box = self._view_factory.placeholder(item=props.side_item).view()
        inner_left_box.native().props.width_request = 200  # TODO ?!?! see also BusyAnimations?!
        inner_left_box.native().props.height_request = 300
        result.append(inner_left_box.native())

        inner_right_box = self._view_factory.placeholder(item=props.main_item).view()
        inner_right_box.native().props.width_request = 300
        result.append(inner_right_box.native())

        return result
