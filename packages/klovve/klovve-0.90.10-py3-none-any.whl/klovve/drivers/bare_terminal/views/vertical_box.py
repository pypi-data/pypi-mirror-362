#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve.pieces.vertical_box


class View(klovve.pieces.vertical_box.View, klovve.BaseView):

    def create_native(self):
        pieces, props = self.make_view()

        class AA:pass
        result = AA()

        @klovve.reaction(owner=result)
        def _():
            self._ff = []
            for item in self.model.items:
                self._ff.append(item.view().native())

        return result
