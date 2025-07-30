#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve.drivers.gtk
import klovve.pieces.split

Gtk = klovve.drivers.gtk.Gtk


class View(klovve.pieces.split.View, klovve.drivers.gtk.View):

    def create_native(self):
        pieces, props = self.make_view()

        paned = self.gtk_new(Gtk.Paned)

        @klovve.reaction(owner=paned)
        def __set_item1():
            if self.model.item1:
                ss = self.model.item1.view().native()
                paned.set_start_child(ss)
                fuh = ss.compute_expand(Gtk.Orientation.HORIZONTAL)  # TODO
                paned.set_resize_start_child(fuh)
            else:
                paned.set_start_child(Gtk.Label(visible=False)) #TODO paned.set_start_child(None)

        @klovve.reaction(owner=paned)
        def __set_item2():
            if self.model.item2:
                ss = self.model.item2.view().native()
                paned.set_end_child(ss)
                fuh = ss.compute_expand(Gtk.Orientation.HORIZONTAL)
                paned.set_resize_end_child(fuh)  # TODO
            else:
                paned.set_end_child(Gtk.Label(visible=False)) #TODO paned.set_end_child(None)

        paned.set_shrink_start_child(False)
        paned.set_shrink_end_child(False)
        return paned
