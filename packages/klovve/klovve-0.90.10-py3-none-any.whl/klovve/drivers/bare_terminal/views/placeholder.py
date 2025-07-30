#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve.pieces.placeholder


class View(klovve.pieces.placeholder.View, klovve.BaseView):

    def create_native(self):
        pieces, props = self.make_view()

        class AA:pass
        result = AA()

        @klovve.reaction(owner=result)
        def _():
            if self.model.item:
                item = self.model.item
                if item:
                    result._foo = item.view().native()

        return result
