#  SPDX-FileCopyrightText: © 2021 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import asyncio

import klovve.data.value_holder
import klovve.view
import klovve.pieces.list
import klovve.pieces.button
import klovve.drivers.gtk.views.button
import klovve.drivers.gtk

Gtk = klovve.drivers.gtk.Gtk


class View(klovve.pieces.list.View, klovve.drivers.gtk.View):

    def create_native(self):
        pieces, props = self.make_view()

        box = self.gtk_new(Gtk.Box, orientation=Gtk.Orientation.VERTICAL, hexpand=False)
        scrolled_window = self.gtk_new(Gtk.ScrolledWindow, hexpand=True, vexpand=True, width_request=100,
                                       hscrollbar_policy=Gtk.PolicyType.NEVER, propagate_natural_height=True)
        box.append(scrolled_window)
        listbox = self.gtk_new(Gtk.ListBox, visible=True)
        scrolled_window.set_child(listbox)
        list_actions_panel = self.gtk_new(Gtk.Box, orientation=Gtk.Orientation.VERTICAL)
        box.append(list_actions_panel)

        def on_row_activated(_, row):
            x = None
            if row:
                idx = row.get_index()
                if idx >= 0:
                    x = idx
            self.model.selected_item = self.model.items[x] if (x is not None) else None

            if (x is not None) and self.model.item_actions:
                popover = Gtk.Popover()
                menu_box = self.gtk_new(Gtk.Box, orientation=Gtk.Orientation.VERTICAL)
                popover.set_child(menu_box)
                def goo(ia):
                    def x(_):
                        popover.popdown()  # TODO noh destroy/remove instead
                        self.___TODO = klovve.app.call_maybe_async_func(
                            ia,
                            context=klovve.drivers.gtk.views.button.ActionContext(box, self._view_factory)
                        )
                    return x
                for item_action in self.model.item_actions:
                    btn = self.gtk_new(Gtk.Button, label=item_action.text)
                    menu_box.append(btn)
                    btn.connect("clicked", goo(item_action.action))
                popover.insert_after(row, None)
                popover.popup()

        listbox.connect("row-activated", on_row_activated)

        _refs = [] #TODO

        @klovve.reaction(owner=box)
        def _handle_selected_item():
            if self.model.selected_item:
                try:
                    v = self.model.items.index(self.model.selected_item)
                except ValueError:
                    return  # TODO
                row = listbox.get_row_at_index(v)
            else:
                row = None
            listbox.select_row(row)

        @klovve.reaction(owner=box)
        def _handle_items():
            with klovve.data.deps.no_dependency_tracking():
                selected_item = self.model.selected_item
            for old_item in klovve.drivers.gtk.children(listbox):
                listbox.remove(old_item)
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
                listbox.append(row)
                if item == selected_item:
                    select_row = i
            listbox.select_row(None if (select_row is None) else listbox.get_row_at_index(select_row))
            if select_row is None:
                with klovve.data.deps.no_dependency_tracking():
                    on_row_activated(None, None)

        @klovve.reaction(owner=box)
        def _handle_list_actions():
            for old_item in klovve.drivers.gtk.children(list_actions_panel):
                list_actions_panel.remove(old_item)
            for list_action in self.model.list_actions:
                list_actions_panel.append(self._view_factory.button(list_action).view().native())
            for aux_control in self.model.aux_controls:
                list_actions_panel.append(aux_control.view().native())

        return box
