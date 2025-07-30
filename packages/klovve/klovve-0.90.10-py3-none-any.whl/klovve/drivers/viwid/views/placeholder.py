#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve.drivers.viwid
import klovve.pieces.placeholder

import viwid.widgets.box


class View(klovve.pieces.placeholder.View, klovve.drivers.viwid.View):

    def create_native(self):
        pieces, props = self.make_view()

        box = viwid.widgets.box.Box()  # TODO

        @klovve.reaction(owner=box)
        def set_item():
            box.children = [self.model.item.view().native()] if self.model.item else []

        return box
