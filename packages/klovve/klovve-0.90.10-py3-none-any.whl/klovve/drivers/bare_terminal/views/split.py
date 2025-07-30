#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve.pieces.split


class View(klovve.pieces.split.View, klovve.BaseView):

    def create_native(self):
        pieces, props = self.make_view()

        class AA:pass
        result = AA()

        @klovve.reaction(owner=result)
        def _():
            if self.model.item1:
                item = self.model.item1
                if item:
                    result._foo = item.view().native()
            if self.model.item2:
                item = self.model.item2
                if item:
                    result._fofo = item.view().native()

        return result
