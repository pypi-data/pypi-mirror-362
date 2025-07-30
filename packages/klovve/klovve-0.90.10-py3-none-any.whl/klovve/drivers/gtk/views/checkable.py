#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve.drivers.gtk
import klovve.pieces.checkable

Gtk = klovve.drivers.gtk.Gtk


class View(klovve.pieces.checkable.View, klovve.drivers.gtk.View):

    def create_native(self):
        pieces, props = self.make_view()

        return self.gtk_new(Gtk.CheckButton, label=props.text, active=props.is_checked)
