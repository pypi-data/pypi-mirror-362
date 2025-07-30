#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve.drivers.gtk
import klovve.pieces.scrollable

Gtk = klovve.drivers.gtk.Gtk


class View(klovve.pieces.scrollable.View, klovve.drivers.gtk.View):

    def create_native(self):
        pieces, props = self.make_view()

        scrolled_window = self.gtk_new(Gtk.ScrolledWindow, hexpand=True, vexpand=True,
                                       hscrollbar_policy=Gtk.PolicyType.NEVER, propagate_natural_height=True)
        box = self.gtk_new(Gtk.Box)
        scrolled_window.set_child(box)

        @klovve.reaction(owner=scrolled_window)
        def _():
            for old_child in klovve.drivers.gtk.children(box):
                box.remove(old_child)
            if self.model.item:
                box.append(self.model.item.view().native())

        return scrolled_window
