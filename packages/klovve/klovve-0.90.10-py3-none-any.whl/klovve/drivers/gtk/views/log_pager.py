#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve.pieces.log_pager
import klovve.drivers.gtk

Gtk = klovve.drivers.gtk.Gtk


class View(klovve.pieces.log_pager.View, klovve.drivers.gtk.View):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__scrolled_to_bottom = True
        self.__scrolled_last_upper = 0

    def create_native(self):
        pieces, props = self.make_view()

        result = self.gtk_new(Gtk.Box, orientation=Gtk.Orientation.VERTICAL, hexpand=True, vexpand=True)

        scrolled_window = self.gtk_new(Gtk.ScrolledWindow, to_parent=result, vexpand=True, width_request=200)

        unfiltered_tree_store = Gtk.TreeStore(str, str, str, bool)
        filtered_tree_store = unfiltered_tree_store.filter_new()
        def is_log_entry_visible(_, iter, __):
            with klovve.data.deps.no_dependency_tracking():  # TODO needed?!
                return (not unfiltered_tree_store.get_value(iter, 3)) or self.model.show_verbose
        filtered_tree_store.set_visible_func(is_log_entry_visible)
        listbox = self.gtk_new(Gtk.TreeView, headers_visible=False, model=filtered_tree_store)
        scrolled_window.set_child(listbox)

        @klovve.reaction(owner=result)
        def TODO():
            _ = self.model.show_verbose
            filtered_tree_store.refilter()

        # TODO    listbox.connect("size-allocate", self.__inner_size_changed)
        # TODO
        klovve.drivers.gtk.GLib.timeout_add(1000, lambda: self.__inner_size_changed(listbox) or True)

        listbox.append_column(Gtk.TreeViewColumn("", Gtk.CellRendererText(), text=0))
        listbox.append_column(Gtk.TreeViewColumn("", Gtk.CellRendererText(), text=1))
        listbox.append_column(Gtk.TreeViewColumn("", Gtk.CellRendererText(), text=2))

        class ItemsObserver(klovve.ListObserver):

            def __init__(self, iter):
                self.__iter = iter

            def item_added(self, index, item):
                new_item_iter = unfiltered_tree_store.insert(self.__iter, index, ["", "", "", item.only_verbose])

                @klovve.reaction(owner=item)
                def _item_from_time():
                    unfiltered_tree_store.set_value(new_item_iter, 0, item.began_at__text)

                @klovve.reaction(owner=item)
                def _item_to_time():
                    unfiltered_tree_store.set_value(new_item_iter, 1, item.ended_at__text)

                @klovve.reaction(owner=item)
                def _item_message():
                    unfiltered_tree_store.set_value(new_item_iter, 2, item.message)

                klovve.data.model.observe_list(item, "entries", ItemsObserver(new_item_iter))

                if self.__iter and unfiltered_tree_store.iter_n_children(self.__iter) == 1:
                    listbox.expand_row(unfiltered_tree_store.get_path(self.__iter), open_all=False)  # TODO works?

            def item_removed(self, index):
                print("TODO r", index)

            def item_moved(self, from_index, to_index):
                print("TODO ra", from_index, to_index)

        klovve.data.model.observe_list(self.model, "entries", ItemsObserver(None))
        return result

    def __inner_size_changed(self, widget, *_):
        adjustment = widget.props.vadjustment
        if self.__scrolled_last_upper == adjustment.props.upper:
            self.__scrolled_to_bottom = (adjustment.props.upper
                                         - adjustment.props.page_size - adjustment.props.value) < 5
        else:
            if self.__scrolled_to_bottom:
                adjustment.props.value = adjustment.props.upper
            self.__scrolled_last_upper = adjustment.props.upper
