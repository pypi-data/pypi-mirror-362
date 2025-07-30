#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve.pieces.tabbed.tab


class View(klovve.pieces.tabbed.tab.View, klovve.ComposedView):

    def compose(self):
        pieces, props = self.make_view()
        return pieces.placeholder(item=props.item)
