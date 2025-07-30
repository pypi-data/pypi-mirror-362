#  SPDX-FileCopyrightText: © 2021 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
"""
Klovve Gtk driver.
"""
import os
import weakref
import selectors
import asyncio
import typing as t

import klovve
import klovve.debug
import klovve.drivers
import klovve.data.value_holder

import gi
gi.require_version("Gtk", "4.0")
from gi.repository import GLib
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf
from gi.repository import GObject
from gi.repository import Pango


class Driver(klovve.drivers.Driver):

    @staticmethod
    def rank():
        return 1_000

    @staticmethod
    def name():
        return "gtk"

    def show_window(self, window):
        window.native().show()

    def _create_mainloop(self):
        return _EventLoop()


class View(klovve.BaseView):

    @staticmethod
    def bind(gobj, gprop_name, value: t.Any):
        if isinstance(value, klovve.data.value_holder.ValueHolder):
            View.__bind(gobj, gprop_name=gprop_name, value_holder=value)
        else:
            gobj.set_property(gprop_name, value)

    @staticmethod
    def __bind(gobj, *, gprop_name, value_holder: klovve.data.value_holder.ValueHolder):

        @klovve.reaction(owner=gobj)  # TODO or owner=obj?!
        def transfer():
            new_source_value = value_holder.get_value()
            getattr(gobj, f"set_{gprop_name}")(new_source_value)
            # TODO memleak        #gobj.set_property(gprop_name, getattr(obj, prop_name))

        if value_holder.is_settable():
            def bar(_, __):
                value_holder.set_value(gobj.get_property(gprop_name))
            gobj.connect(f"notify::{gprop_name}", bar)

    @staticmethod
    def gtk_new(viewtype, *, to_parent=None, **kwargs):  # TODO
        d1 = {}
        d2 = {}
        for k, v in kwargs.items():
            if isinstance(v, klovve.data.value_holder.ValueHolder): # TODO dedup ?!
                d1[k] = v
            else:
                d2[k] = v
        widget = viewtype(**d2)
        klovve.debug.memory.new_object_created(widget, "Gtk.Widget")
        for k, v in d1.items():
            View.__bind(widget, gprop_name=k, value_holder=v)
        # TODO ?!
        #  widget._ref_sink()
        # widget._unref()
        if to_parent:
            to_parent.append(widget)
        return widget

    @staticmethod
    def gtk_children(widget):
        return children(widget)


def children(widget):
    result = []
    child = widget.get_first_child()
    while child:
        result.append(child)
        child = child.get_next_sibling()
    return result


class _EventLoop(asyncio.SelectorEventLoop):

    def __init__(self):
        self.__selector = _Selector(GLib.MainContext.default())
        super().__init__(self.__selector)

    def _call_soon(self, callback, args, context):
        result = super()._call_soon(callback, args, context)
        self.__selector.interrupt_glib_mainloop()
        return result

    def call_at(self, when, callback, *args, context=None):
        result = super().call_at(when, callback, *args, context=context)
        self.__selector.interrupt_glib_mainloop()
        return result

    def create_task(self, coro, *, name=None):
        result = super().create_task(coro, name=name)
        self.__selector.interrupt_glib_mainloop()
        return result


class _Selector(selectors._BaseSelectorImpl):

    def __init__(self, context):
        super().__init__()
        self.__glib_mainloop = GLib.MainLoop(context)
        self.__glib_mainloop_run = getattr(super(GLib.MainLoop, GLib.MainLoop), "run", GLib.MainLoop.run)
        self.__glib_event_source = _Source(self.__glib_mainloop)
        self.__glib_event_source.attach(context)

    def close(self):  # TODO order
        super().close()
        self.__glib_event_source.destroy()

    def register(self, fileobj, events, data=None):
        result = super().register(fileobj, events, data)
        self.__glib_event_source.add_fd(result.fd, events)
        return result

    def unregister(self, fileobj):
        result = super().unregister(fileobj)
        self.__glib_event_source.remove_fd(result.fd)
        return result

    def select(self, timeout=None):
        if (timeout is None) or (timeout > 0):
            self.__glib_event_source.set_ready_time(
                -1 if (timeout is None) else int(GLib.get_monotonic_time() + 1000000 * timeout))
            self.__glib_mainloop_run(self.__glib_mainloop)
        else:
            self.__glib_mainloop.get_context().iteration(False)
        return [(key, events) for key, events in
                [(key, self.__glib_event_source.get_events(key.fd) & key.events) for key in self.get_map().values()]
                if events]

    def interrupt_glib_mainloop(self):
        self.__glib_event_source.set_ready_time(0)


class _Source(GLib.Source):

    EVENT_TO_GLIB = {selectors.EVENT_READ: GLib.IOCondition.IN, selectors.EVENT_WRITE: GLib.IOCondition.OUT}.items()

    def __init__(self, main_loop):
        super().__init__()
        self.__fd_tags = {}
        self.__fd_events = {}  # TODO cleanup
        self.__main_loop = main_loop

    def prepare(self):
        return False, -1

    def check(self):
        return False

    def dispatch(self, callback, args):
        for fd, tag in self.__fd_tags.items():
            self.__fd_events[fd] = self.__fd_events.get(fd, 0) | self.__glib_to_python_events(self.query_unix_fd(tag))
        self.__main_loop.quit()
        return GLib.SOURCE_CONTINUE

    def get_events(self, fd):
        return self.__fd_events.get(fd, 0)

    def add_fd(self, fd, events):
        self.__fd_tags[fd] = self.add_unix_fd(fd, self.__python_to_glib_events(events))

    def remove_fd(self, fd):
        self.remove_unix_fd(self.__fd_tags.pop(fd))
        if fd in self.__fd_events:
            self.__fd_events.pop(fd)

    def __glib_to_python_events(self, glib_events):
        python_events = 0
        for event, glib_event in self.EVENT_TO_GLIB:
            if glib_events & glib_event:
                python_events |= event
        return python_events

    def __python_to_glib_events(self, python_events):
        glib_events = GLib.IOCondition(0)
        for python_event, glib_event in self.EVENT_TO_GLIB:
            if python_events & python_event:
                glib_events |= glib_event
        return glib_events
