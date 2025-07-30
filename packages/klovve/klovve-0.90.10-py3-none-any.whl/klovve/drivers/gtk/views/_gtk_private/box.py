#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve.drivers.gtk
import klovve.pieces.horizontal_box

Gtk = klovve.drivers.gtk.Gtk


class View(klovve.drivers.gtk.View):

    def _orientation(self):
        raise NotImplementedError()

    def create_native(self):
        pieces, props = self.make_view()

        box = self.gtk_new(Gtk.Box, orientation=self._orientation())

        class ItemsObserver(klovve.ListObserver):

            def item_added(self, index, item):
                item_widget = item.view().native()
                ch = klovve.drivers.gtk.children(box)
                if index == len(ch):
                    box.append(item_widget)
                else:
                    item_widget.insert_before(box, ch[index])

            def item_removed(self, index):
                box.remove(klovve.drivers.gtk.children(box)[index])

            def item_moved(self, from_index, to_index):
                ch = klovve.drivers.gtk.children(box)
                mm = klovve.drivers.gtk.children(box)[from_index]
                if to_index == len(ch):
                    box.append(mm)
                else:
                    mm.insert_before(box, ch[to_index])

        klovve.data.model.observe_list(self.model, "items", ItemsObserver())

        return box
