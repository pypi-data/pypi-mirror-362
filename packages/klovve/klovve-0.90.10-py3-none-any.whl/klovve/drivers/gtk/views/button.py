#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import asyncio

import klovve.app.context
import klovve.data.value_holder
import klovve.pieces.button
import klovve.drivers.gtk
import klovve.view

Gtk = klovve.drivers.gtk.Gtk


class View(klovve.pieces.button.View, klovve.drivers.gtk.View):

    def create_native(self):
        pieces, props = self.make_view()

        button = self.gtk_new(Gtk.Button, hexpand=True, halign=Gtk.Align.CENTER, label=props(twoway=False).text)

        def X(t):
            self.___TODO = t
            return t
        button.connect("clicked", lambda _: X(klovve.app.call_maybe_async_func(
            self.model.action,
            context=ActionContext(button, self._view_factory)
        )))

        return button


class ActionContext(klovve.app.context.ActionContext):

    def __init__(self, button, *args):
        super().__init__(*args)
        self.__button = button

    async def _create_dialog(self, view, done_future):#TODO dedup
        popover = Gtk.Popover() # TODO relative_to=self.__button)
        popover.set_child(view.native())
        popover.insert_after(self.__button, None)
        popover.popup()  # TODO kaputt
        await done_future
        popover.popdown()

