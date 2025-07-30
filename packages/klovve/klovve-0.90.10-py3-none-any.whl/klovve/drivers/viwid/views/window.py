#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import asyncio
import contextlib
import traceback
import klovve.app.context
import klovve.drivers.viwid
import klovve.pieces.window

import viwid.widgets.box
import viwid.widgets.button
import viwid.widgets.label


class View(klovve.pieces.window.View, klovve.drivers.viwid.View):

    def create_native(self):
        pieces, props = self.make_view()

        hdlabel = viwid.widgets.label.Label()
#        hdlabel.set_root_style(self.screen.style.)
        hdibox = viwid.widgets.box.Box(
            children=[viwid.widgets.label.Label(text="  ", horizontal_expand_greedily=True),
                      hdlabel,
                      viwid.widgets.label.Label(text="  ", horizontal_expand_greedily=True),
                      viwid.widgets.button.Button(text="Exit")],
            orientation=viwid.widgets.box.Orientation.HORIZONTAL,
        )
        hdbox = viwid.widgets.box.Box(
            orientation=viwid.widgets.box.Orientation.HORIZONTAL,
            children=[hdibox],
            horizontal_expand_greedily=True,
        )
        window = viwid.widgets.box.Box()

        box = viwid.widgets.box.Box(
            children=[hdbox,window],
            orientation=viwid.widgets.box.Orientation.VERTICAL
        )






        #window = self.WidgetPlaceholder()#TODO, title=model_bind(twoway=False).title,
                                      #screen=klovve.drivers.urwid.screeN, height=31, width=31)

        @klovve.reaction(owner=self)
        def ff():
            if self.model.is_closed:
                pass#TODO

        @klovve.reaction(owner=self)
        def fsf():
            hdlabel.text = self.model.title or ""

        """
        async def do():
            do_close = klovve.app.call_with_kwargs_maybe_async(
                model.close_func or (lambda context: True), asyncio.get_running_loop(),
                context=Context(self._view_factory, window)
            )
            if inspect.isawaitable(do_close):  # TDO
                do_close = await do_close
            if do_close:
              #TDO needed?  for foo in klovve.drivers.gtk.children(window):
               #     window.remove(foo)
                model.is_closed = True
                window.destroy()

        window.connect("close-request", lambda *_: klovve.drivers.gtk.GLib.idle_add(
            lambda: klovve.app.call_with_kwargs_maybe_async(
                do, asyncio.get_running_loop()
            ) and False# TDO needed for idle_add
        ) or True)
TODO
"""
        @klovve.reaction(owner=window)
        def set_body():
            window.children = [self.model.body.view().native()] if self.model.body else []

        return box
       # return urwid.Filler(window, valign="top")


class ActionContext(klovve.app.context.ActionContext):

    def __init__(self, main_window, *args):
        super().__init__(*args)
        self.__main_window = main_window

    async def _create_dialog(self, view, done_future):#TODO dedup
        gtk = klovve.drivers.gtk.Gtk
        dialog = gtk.Window(transient_for=self.__main_window, modal=True)
        dialog.append(view.native())
        dialog.show()
        await done_future
        dialog.destroy()
