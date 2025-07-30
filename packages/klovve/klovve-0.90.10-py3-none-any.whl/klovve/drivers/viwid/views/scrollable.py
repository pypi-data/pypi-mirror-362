#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve.drivers.viwid
import klovve.pieces.scrollable

import viwid.widgets.scrollable


class View(klovve.pieces.scrollable.View, klovve.drivers.viwid.View):

    def create_native(self):
        pieces, props = self.make_view()

        box = viwid.widgets.scrollable.Scrollable(
            horizontal_expand_greedily=True,
            vertical_expand_greedily=True,
        )

        @klovve.reaction(owner=box)
        def set_item():
            if self.model.item:
                box.item = self.model.item.view().native()
            else:
                box.item = None

        return box
