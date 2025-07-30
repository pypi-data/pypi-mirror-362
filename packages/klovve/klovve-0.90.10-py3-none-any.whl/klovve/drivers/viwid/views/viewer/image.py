#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import pathlib
import klovve.drivers.viwid
import klovve.pieces.viewer.image

import viwid.widgets.label


class View(klovve.pieces.viewer.image.View, klovve.drivers.viwid.View):

    def create_native(self):
        pieces, props = self.make_view()

        return viwid.widgets.label.Label()
