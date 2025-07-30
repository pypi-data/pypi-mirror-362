#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import sys

import klovve.pieces.log_pager


class View(klovve.pieces.log_pager.View, klovve.BaseView):

    def create_native(self):
        pieces, props = self.make_view()

        class AA:pass
        result = AA()

        class ItemsObserver(klovve.ListObserver):

            def item_added(self, index, item):

                @klovve.reaction(owner=item)
                def _item_message():
                    if item.message:
                        print(item.message, file=sys.stderr)

                klovve.data.model.observe_list(item, "entries", ItemsObserver())

            def item_removed(self, index):
                pass

            def item_moved(self, from_index, to_index):
                pass

        klovve.data.model.observe_list(self.model, "entries", ItemsObserver())

        return result
