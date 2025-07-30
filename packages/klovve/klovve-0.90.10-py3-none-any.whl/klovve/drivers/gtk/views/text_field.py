#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve.drivers.gtk
import klovve.pieces.text_field

Gtk = klovve.drivers.gtk.Gtk


class View(klovve.pieces.text_field.View, klovve.drivers.gtk.View):

    def create_native(self):
        pieces, props = self.make_view()

        return self.gtk_new(Gtk.Entry, text=props.text, placeholder_text=props(twoway=False).hint_text)
