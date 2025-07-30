#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import asyncio

import viwid.widgets.list
import viwid.widgets.scrollable
import viwid.widgets.label

import klovve.pieces.log_pager
import klovve.drivers.viwid


class View(klovve.pieces.log_pager.View, klovve.drivers.viwid.View):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__scrolled_to_bottom = True
        self.__scrolled_last_upper = 0

    def create_native(self):
        pieces, props = self.make_view()

        listbox = viwid.widgets.list.List()

        class ItemsObserver(klovve.ListObserver):

            def __init__(self, iter):
                self.__iter = iter

            def item_added(self, index, item):
                tx = viwid.widgets.list.ListRow()

                @klovve.reaction(owner=item)
                def _item_message():
                    beg = item.began_at__text.ljust(13, " ")
                    end = item.ended_at__text.ljust(13, " ")  # TODO ljust hack
                    tx.text = beg + end + item.message

                if not item.only_verbose:#TODO
                    listbox.items.append(tx)
                    listbox.items = listbox.items
                    klovve.data.model.observe_list(item, "entries", ItemsObserver(123))

            def item_removed(self, index):
                print("TODO r", index)

            def item_moved(self, from_index, to_index):
                print("TODO ra", from_index, to_index)

        klovve.data.model.observe_list(self.model, "entries", ItemsObserver(None))

        scrollable = viwid.widgets.scrollable.Scrollable(item=listbox)

        #TODO    listbox.connect("size-allocate", self.__inner_size_changed)
        #TODO
        def xx():
            self.__inner_size_changed(scrollable)
            asyncio.get_running_loop().call_later(1, xx)
        xx()

        return scrollable

    def __inner_size_changed(self, scrollable: viwid.widgets.scrollable.Scrollable):
        newy = min(0, scrollable.size.height - scrollable.inner_size.height)
        if self.__scrolled_last_upper == newy:
            self.__scrolled_to_bottom = (scrollable.inner_size.height - scrollable.size.height + scrollable.offset.y) <= 0
        else:
            if self.__scrolled_to_bottom:
                scrollable.set_offset(viwid.Point(scrollable.offset.x, newy))
            self.__scrolled_last_upper = newy


def _time_text(d):
    if not d:
        return ""
    return d.strftime("%X")
