#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve.drivers.viwid
import klovve.pieces.text_field

import viwid.widgets.check_button


class View(klovve.pieces.text_field.View, klovve.drivers.viwid.View):

    def create_native(self):
        pieces, props = self.make_view()

        result = viwid.widgets.check_button.CheckButton()

        @klovve.reaction(owner=result)
        def __set_result_text():
            result.text = self.model.text

        def __set_model_text():
            self.model.text = result.text

        result.listen_property("text", __set_model_text)

        return result


