#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import asyncio
import inspect
import os

import klovve.app.context
import klovve.drivers.gtk
import klovve.pieces.window

Gtk = klovve.drivers.gtk.Gtk


class View(klovve.pieces.window.View, klovve.drivers.gtk.View):

    def create_native(self):
        pieces, props = self.make_view()

        window = self.gtk_new(klovve.drivers.gtk.Gtk.Window, title=props(twoway=False).title)  # TODO gtk main window / appl. wnd.?

        css_provider = Gtk.CssProvider()
        css_provider.load_from_path(f"{os.path.dirname(__file__)}/-data/main.css")
        Gtk.StyleContext.add_provider_for_display(klovve.drivers.gtk.Gdk.Display.get_default(), css_provider,
                                                  Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        @klovve.reaction(owner=self)
        def ff():
            if self.model.is_closed:
                window.destroy()

        async def do():
            do_close = await klovve.app.call_maybe_async_func(
                self.model.close_func or (lambda context: True),
                context=ActionContext(window, self._view_factory)
            )
            if do_close:
              #TODO needed?  for foo in klovve.drivers.gtk.children(window):
               #     window.remove(foo)
                self.model.is_closed = True

        def ddo(_):
            self.___TODO = asyncio.get_running_loop().create_task(do())
            return True

        window.connect("close-request", ddo)

        @klovve.reaction(owner=window)
        def set_body():
            window.set_child(self.model.body.view().native())

        return window


class ActionContext(klovve.app.context.ActionContext):

    def __init__(self, main_window, *args):
        super().__init__(*args)
        self.__main_window = main_window

    async def _create_dialog(self, view, done_future):#TODO dedup
        dialog = Gtk.Window(transient_for=self.__main_window, modal=True)
        dialog.append(view.native())
        dialog.show()
        await done_future
        dialog.destroy()
