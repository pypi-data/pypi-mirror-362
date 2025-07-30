# SPDX-FileCopyrightText: © 2025 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only
import functools

import klovve.builtin.drivers.viwid
import klovve.data
import klovve.variable

import viwid


class Tabbed(klovve.builtin.drivers.viwid.ViewMaterialization[klovve.views.Tabbed]):

    def create_native(self):
        viwid_tabbed = self.new_native(viwid.widgets.tabbed.Tabbed, self.piece)

        self.piece._introspect.observe_list_property(klovve.views.Tabbed.tabs, self.__ItemsObserver,
                                                     (self, viwid_tabbed,), owner=self)
        klovve.effect.activate_effect(self.__refresh_current_tab_in_ui, (viwid_tabbed,), owner=viwid_tabbed)
        viwid_tabbed.listen_property("active_tab", lambda *_: self.__refresh_current_tab_in_model(viwid_tabbed))

        return viwid_tabbed

    def __refresh_current_tab_in_ui(self, viwid_tabbed: viwid.widgets.tabbed.Tabbed) -> None:
        if current_tab := self.piece.current_tab:
            with klovve.variable.no_dependency_tracking():
                if (current_tab_idx := self.piece.tabs.index(current_tab)) >= 0:
                    viwid_tabbed.active_tab_index = current_tab_idx

    def __refresh_current_tab_in_model(self, viwid_tabbed: viwid.widgets.tabbed.Tabbed) -> None:
        current_tab_idx = viwid_tabbed.active_tab_index
        if len(self.piece.tabs) > current_tab_idx:
            self.piece.current_tab = self.piece.tabs[current_tab_idx]

    class __ItemsObserver(klovve.data.list.List.Observer):

        def __init__(self, tabbed: "Tabbed", viwid_tabbed: viwid.widgets.tabbed.Tabbed):
            super().__init__()
            self.__tabbed = tabbed
            self.__viwid_tabbed = viwid_tabbed

        def item_added(self, index, item):
            viwid_tab = viwid.widgets.tabbed.Tabbed.Tab()
            self.__viwid_tabbed.tabs.insert(index, viwid_tab)

            viwid_tab.listen_event(viwid.widgets.tabbed.Tabbed.Tab.RequestCloseEvent,
                                   functools.partial(self.__handle_request_close_tab, item))
            klovve.effect.activate_effect(self.__refresh_label_in_ui, (item, viwid_tab), owner=viwid_tab)
            klovve.effect.activate_effect(self.__refresh_close_button_visibility_in_ui, (item, viwid_tab), owner=viwid_tab)
            klovve.effect.activate_effect(klovve.builtin.drivers.viwid.ViewMaterialization.MaterializingViewEffect,
                                          (self.__tabbed, viwid_tab, lambda: item.body), owner=viwid_tab)

        def item_removed(self, index, item):
            self.__viwid_tabbed.tabs.pop(index)

        def __handle_request_close_tab(self, tab, event):
            self.__tabbed.piece.request_close(tab)
            event.stop_handling()

        def __refresh_label_in_ui(self, tab: klovve.views.Tabbed.Tab, viwid_tab):
            viwid_tab.title = tab.title

        def __refresh_close_button_visibility_in_ui(self, tab: klovve.views.Tabbed.Tab, viwid_tab):
            viwid_tab.is_closable_by_user = tab.is_closable
