#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve.drivers.viwid
import klovve.pieces.property_panel

import viwid.widgets.label


class View(klovve.pieces.property_panel.View, klovve.drivers.viwid.View):

    def create_native(self):
        pieces, props = self.make_view()

        self.model.values["hostname"] = "nnn"
        return viwid.widgets.label.Label(text="TODO")
