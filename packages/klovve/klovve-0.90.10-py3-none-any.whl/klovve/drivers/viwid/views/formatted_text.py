#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve.drivers.viwid
import klovve.pieces.formatted_text
import xml.etree.ElementTree

import viwid.widgets.label


class View(klovve.pieces.formatted_text.View, klovve.drivers.viwid.View):

    def create_native(self):  # TODO scrolling?!
        pieces, props = self.make_view()

        label = viwid.widgets.label.Label()

        @klovve.reaction(owner=label)
        def tx():
            if self.model.text:
                x = xml.etree.ElementTree.fromstring(f"<x>{self.model.text}</x>")
                text = ""
                ul = 0
                def ca(ele):
                    nonlocal text, ul
                    if ele.tag == "br":
                        text += "\n"
                    if ele.tag == "h1":
                        text += "\n"
                    if ele.tag == "ul":
                        ul += 1
                        text += "\n\n"
                    if ele.tag == "li":
                        text += "- "
                    text += ele.text or ""
                    for child in ele:
                        ca(child)
                    if ele.tag == "ul":
                        ul -= 1
                        text += "\n"
                    if ele.tag == "h1":
                        text += "\n\n"
                    if ele.tag == "li":
                        text += "\n"
                    text += ele.tail or ""
                ca(x)
                label.text = text
            else:
                label.text = ""

        return label
