#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve.drivers.gtk
import klovve.pieces.header

Gtk = klovve.drivers.gtk.Gtk


class View(klovve.pieces.header.View, klovve.drivers.gtk.View):

    def create_native(self):
        pieces, props = self.make_view()

        return self.gtk_new(Gtk.Label, wrap=True, label=props(twoway=False).text, css_classes=["klovve_header"])
