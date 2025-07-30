#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import asyncio

import klovve.app.context
import klovve.pieces.button
import klovve.data.value_holder
import klovve.drivers.viwid

import viwid.widgets.button
import viwid.widgets.box
import viwid.screen


class View(klovve.pieces.button.View, klovve.drivers.viwid.View):

    def create_native(self):
        pieces, props = self.make_view()

        button = viwid.widgets.button.Button()

        @klovve.reaction(owner=button)
        def __set_button_text():
            button.text = self.model.text

        def X(t):
            self.___TODO = t
            return t
        button.on_click.append(lambda: X(klovve.app.call_maybe_async_func(
            self.model.action,
            context=ActionContext(button, self._view_factory)
        )))

        return button


class ActionContext(klovve.app.context.ActionContext):

    def __init__(self, button, *args):
        super().__init__(*args)
        self.__button = button

    async def _create_dialog(self, view, done_future):#TODO dedup
        popover = viwid.widgets.box.Box(children=[view.native()])
        closer = self.__button.screen.popup(popover,
                                    alignment=viwid.screen.RootAlignment(
                                        viwid.screen.AnchorRootAlignmentPositioning(self.__button),
                                        viwid.screen.AnchorRootAlignmentPositioning(self.__button),
                                        viwid.screen.AutoRootAlignmentSizing(),
                                        viwid.screen.AutoRootAlignmentSizing()
                                    ))
        await done_future
        closer()
