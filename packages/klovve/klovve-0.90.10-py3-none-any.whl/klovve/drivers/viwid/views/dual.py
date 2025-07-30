#  SPDX-FileCopyrightText: © 2021 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve.pieces.dual
import klovve.drivers.viwid


class View(klovve.pieces.dual.View, klovve.drivers.viwid.View):

    def create_native(self):
        pieces, props = self.make_view()

        gtk = klovve.drivers.gtk.Gtk
        box = self.gtk_new(gtk.Box, orientation=gtk.Orientation.HORIZONTAL)
        inner_left_box = self._view_factory.placeholder(item=props.side_item).view()
        inner_right_box = self._view_factory.placeholder(item=props.main_item).view()
        inner_left_box.native().props.width_request = 200
        inner_left_box.native().props.height_request = 300
        inner_right_box.native().props.width_request = 300
        box.append(inner_left_box.native())
        box.append(inner_right_box.native())
        return box
