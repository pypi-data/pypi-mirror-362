#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve.drivers.gtk
import klovve.pieces.label

Gtk = klovve.drivers.gtk.Gtk


class View(klovve.pieces.label.View, klovve.drivers.gtk.View):

    def create_native(self):
        pieces, props = self.make_view()

        return self.gtk_new(Gtk.Label, wrap=True, hexpand=True, vexpand=True, label=props.text)
