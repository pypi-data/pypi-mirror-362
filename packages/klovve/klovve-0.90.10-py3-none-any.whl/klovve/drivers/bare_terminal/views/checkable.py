#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve.pieces.checkable


class View(klovve.pieces.checkable.View, klovve.BaseView):

    def create_native(self):
        pieces, props = self.make_view()

        class AA:pass
        result = AA()

        return result
