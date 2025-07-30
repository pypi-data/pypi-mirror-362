#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve.drivers.viwid
import klovve.pieces.label

import viwid.widgets.label


class View(klovve.pieces.label.View, klovve.drivers.viwid.View):

    def create_native(self):
        pieces, props = self.make_view()

        result = viwid.widgets.label.Label()

        @klovve.reaction(owner=result)
        def TODO():
            result.text = self.model.text

        return result
