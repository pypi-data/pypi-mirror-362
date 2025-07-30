#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve.pieces.dropdown
import klovve.drivers.gtk

Gtk = klovve.drivers.gtk.Gtk


class View(klovve.pieces.dropdown.View, klovve.drivers.gtk.View):

    def create_native(self):
        pieces, props = self.make_view()

        tree_store = Gtk.TreeStore(str)

        combo_box = self.gtk_new(Gtk.ComboBox, hexpand=True, halign=Gtk.Align.CENTER, model=tree_store)

        cell_renderer = Gtk.CellRendererText(text=0)
        combo_box.pack_start(cell_renderer, True)
        combo_box.add_attribute(cell_renderer, 'text', 0)

        def foo(w):
            x = None
            idx = combo_box.get_active()
            if idx >= 0:
                x = idx
            self.model.selected_item = self.model.items[x] if (x is not None) else None
        combo_box.connect("changed", foo)

        _refs = []  # TODO

      #  @klovve.reaction(owner=tree_store)
        def _handle_items():
            selected_item = self.model.selected_item
            #for olditem in self.combo_box.get_children():
            #    self.combo_box.remove(olditem)
            item_label_func = (self.model.item_label_func or str)
            select_row = None
            _refs.clear()
            def bla(ll, itm):
                @klovve.reaction(owner=None)
                def flg():
                    vv = item_label_func(itm)
                    ll.props.label = vv
                return flg
            for i, item in enumerate(self.model.items):
                row = Gtk.Label(xalign=0, visible=True)
                _refs.append(row)
                _refs.append(bla(row, item))
                combo_box.append(row)
                if item == selected_item:
                    select_row = i
            combo_box.select_row(None if (select_row is None) else combo_box.get_row_at_index(select_row))
            if select_row is None:
                foo(None, None)

   #     @klovve.reaction(owner=tree_store)
        def _handle_selection():
            selected_item = self.model.selected_item
            select_row = -1
            for i, item in enumerate(self.model.items):
                if item == selected_item:
                    select_row = i
                    break
            combo_box.set_active(select_row)
            if select_row is None:
                foo(None)

        item_label_func = (self.model.item_label_func or str)

        class ItemsObserver(klovve.ListObserver):

            def item_added(self, index, item):
                newitemiter = tree_store.insert(None, index, [""])

                #@klovve.reaction(owner=item)
                def _item_message():
                    tree_store.set_value(newitemiter, 0, item_label_func(item))
                _item_message()

            def item_removed(self, index):
                tree_store.remove(tree_store.iter_nth_child(None, index))

            def item_moved(self, from_index, to_index):
                print("TODO rca", from_index, to_index)

        klovve.data.model.observe_list(self.model, "items", ItemsObserver())

        return combo_box
