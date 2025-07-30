#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve.drivers.gtk
import klovve.pieces.placeholder

Gtk = klovve.drivers.gtk.Gtk


class View(klovve.pieces.placeholder.View, klovve.drivers.gtk.View):

    def create_native(self):
        pieces, props = self.make_view()

        box = self.gtk_new(Gtk.Box)

        @klovve.reaction(owner=box)
        def __set_item():
            for old_child in self.gtk_children(box):
                box.remove(old_child)
            if self.model.item:
                TODO = self.model.item.view().native()

                #try:
                    #TODO weg
           ####     TODO.unparent()#TODO NOH !?
                #except:
                #    pass

                if not isinstance(TODO, Gtk.Window):
                    box.append(TODO)

        return box
