#  SPDX-FileCopyrightText: © 2021 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import sys
import klovve.pieces.interact.abstract


class View(klovve.pieces.interact.abstract.View, klovve.BaseView):

    def create_native(self):
        pieces, props = self.make_view()

        class AA:pass
        result = AA()

        # TODO
        print(self.model.message, file=sys.stderr)
        if len(self.model.triggers) == 1:
            self.model.answer = True

        return result
