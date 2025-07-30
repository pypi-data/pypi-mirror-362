#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve.drivers.viwid
import klovve.pieces.viewer.pdf

import viwid.widgets.label


class View(klovve.pieces.viewer.pdf.View, klovve.drivers.viwid.View):

    def create_native(self):
        pieces, props = self.make_view()

        return viwid.widgets.label.Label(text=f"Please find the Krrez documentation here:\n\nfile://{self.model.path}")
