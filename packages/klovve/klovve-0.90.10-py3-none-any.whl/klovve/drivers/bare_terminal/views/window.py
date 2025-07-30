#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve.pieces.window


class View(klovve.pieces.window.View, klovve.BaseView):

    def create_native(self):
        pieces, props = self.make_view()

        class AA:pass
        result = AA()

        @klovve.reaction(owner=result)
        def _():
            if self.model.body:
                item = self.model.body
                if item:
                    result._foo = item.view().native()

        return result
