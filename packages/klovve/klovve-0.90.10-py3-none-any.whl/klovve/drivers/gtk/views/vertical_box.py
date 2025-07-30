#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve.drivers.gtk.views._gtk_private.box
import klovve.pieces.vertical_box

Gtk = klovve.drivers.gtk.Gtk


class View(klovve.pieces.vertical_box.View, klovve.drivers.gtk.views._gtk_private.box.View):

    def _orientation(self):
        return Gtk.Orientation.VERTICAL
