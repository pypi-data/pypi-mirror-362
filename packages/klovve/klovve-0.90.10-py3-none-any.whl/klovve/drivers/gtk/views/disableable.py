#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve.drivers.gtk
import klovve.pieces.disableable

Gtk = klovve.drivers.gtk.Gtk


class View(klovve.pieces.disableable.View, klovve.drivers.gtk.View):

    @klovve.ComputedProperty
    def gtk_sensitive(self):
        return not self.model.is_disabled

    def create_native(self):
        pieces, props = self.make_view()

        box = self.gtk_new(Gtk.Box, sensitive=props.gtk_sensitive)

        @klovve.reaction(owner=box)
        def set_item():
            for old_child in klovve.drivers.gtk.children(box):
                box.remove(old_child)
            if self.model.item:
                box.append(self.model.item.view().native())

        return box
