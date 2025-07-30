# SPDX-FileCopyrightText: © 2025 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only
import functools

import klovve.builtin.drivers.gtk
import klovve.data
import klovve.variable
from klovve.builtin.drivers.gtk import Gtk


class Tabbed(klovve.builtin.drivers.gtk.ViewMaterialization[klovve.views.Tabbed]):

    def create_native(self):
        gtk_notebook = self.new_native(Gtk.Notebook, self.piece, scrollable=True)

        self.piece._introspect.observe_list_property(klovve.views.Tabbed.tabs, self.__ItemsObserver,
                                                     (self, gtk_notebook,), owner=self)
        klovve.effect.activate_effect(self.__refresh_current_tab_in_ui, (gtk_notebook,), owner=gtk_notebook)
        gtk_notebook.connect("notify::page", lambda *_: self.__refresh_current_tab_in_model(gtk_notebook))

        return gtk_notebook

    def __refresh_current_tab_in_ui(self, gtk_notebook):
        if current_tab := self.piece.current_tab:
            with klovve.variable.no_dependency_tracking():
                if (current_tab_idx := self.piece.tabs.index(current_tab)) >= 0:
                    gtk_notebook.set_current_page(current_tab_idx)

    def __refresh_current_tab_in_model(self, gtk_notebook):
        current_tab_idx = gtk_notebook.get_current_page()
        if len(self.piece.tabs) > current_tab_idx:
            self.piece.current_tab = self.piece.tabs[current_tab_idx]

    class __ItemsObserver(klovve.data.list.List.Observer):

        def __init__(self, tabbed, gtk_notebook):
            super().__init__()
            self.__tabbed = tabbed
            self.__gtk_notebook = gtk_notebook

        def item_added(self, index, item):
            self.__gtk_notebook.insert_page(
                gtk_tab_body := Gtk.Box(hexpand=True, vexpand=True, hexpand_set=True, vexpand_set=True,
                                        halign=Gtk.Align.FILL, valign=Gtk.Align.FILL, layout_manager=Gtk.BinLayout()),
                gtk_tab_label_box := Gtk.Box(), index)
            gtk_tab_label_box.append(gtk_tab_label_label := Gtk.Label())
            gtk_tab_label_box.append(gtk_tab_label_close_button := Gtk.Button(
                can_focus=False, has_frame=False, icon_name="window-close"))

            gtk_tab_label_close_button.connect("clicked", lambda *_: self.__tabbed.piece.request_close(item))
            klovve.effect.activate_effect(self.__refresh_label_in_ui,
                                          (item, gtk_tab_label_label), owner=gtk_tab_label_label)
            klovve.effect.activate_effect(self.__refresh_close_button_visibility_in_ui,
                                          (item, gtk_tab_label_close_button), owner=gtk_tab_label_close_button)
            klovve.effect.activate_effect(klovve.builtin.drivers.gtk.ViewMaterialization.MaterializingViewEffect,
                                          (self.__tabbed, gtk_tab_body, lambda: item.body), owner=gtk_tab_body)

        def item_removed(self, index, item):
            self.__gtk_notebook.remove_page(index)

        def __refresh_label_in_ui(self, tab: klovve.views.Tabbed.Tab, gtk_label):
            gtk_label.set_label(tab.title)

        def __refresh_close_button_visibility_in_ui(self, tab: klovve.views.Tabbed.Tab, gtk_button):
            gtk_button.set_visible(tab.is_closable)
