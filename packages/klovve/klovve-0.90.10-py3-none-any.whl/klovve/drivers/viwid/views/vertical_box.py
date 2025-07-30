#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve.drivers.viwid.views._curses_private.box
import klovve.pieces.vertical_box


class View(klovve.pieces.vertical_box.View, klovve.drivers.viwid.views._curses_private.box.View):

    def _orientation(self):
        return 2
