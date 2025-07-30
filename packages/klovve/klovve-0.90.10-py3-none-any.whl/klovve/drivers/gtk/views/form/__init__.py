#  SPDX-FileCopyrightText: © 2021 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve.pieces.form
import klovve.drivers.gtk

Gtk = klovve.drivers.gtk.Gtk


class View(klovve.pieces.form.View, klovve.drivers.gtk.View):

    def create_native(self):
        pieces, props = self.make_view()

        result = self.gtk_new(Gtk.Box, orientation=Gtk.Orientation.VERTICAL, hexpand=True, vexpand=True,
                              halign=Gtk.Align.CENTER, valign=Gtk.Align.CENTER)

        @klovve.reaction(owner=self)
        def __on_items_changed():
            for old_child in klovve.drivers.gtk.children(result):
                result.remove(old_child)
            for item in self.model.items:
                result.append(item.view().native())

        return result
