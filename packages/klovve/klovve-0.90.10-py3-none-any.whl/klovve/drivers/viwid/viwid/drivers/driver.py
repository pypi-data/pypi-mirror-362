#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import abc
import importlib.util
import pkgutil
import typing as t
import viwid.canvas
import viwid.widgets.widget
import viwid.screen
import viwid.loop


class Driver(abc.ABC):

    @property
    @abc.abstractmethod
    def loop(self) -> viwid.loop.Loop:
        pass

    @property
    @abc.abstractmethod
    def screens(self) -> t.Iterable[viwid.screen.Screen]:
        pass

    @abc.abstractmethod
    def add_widget_screen(self, widget: viwid.widgets.widget.Widget) -> viwid.screen.Screen:
        pass

    @abc.abstractmethod
    def repaint_widget_soon(self, widget: viwid.widgets.widget.Widget) -> None:
        pass

    @abc.abstractmethod
    def resize_widget_soon(self, widget: viwid.widgets.widget.Widget) -> None:
        pass

    @abc.abstractmethod
    def canvas(self, widget: viwid.widgets.widget.Widget) -> viwid.canvas.Canvas:
        pass
