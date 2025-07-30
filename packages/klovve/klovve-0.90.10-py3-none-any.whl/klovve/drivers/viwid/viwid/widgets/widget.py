#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import asyncio
import enum
import functools
import sys
import typing as t

import viwid.canvas
import viwid.data
#import viwid.screen
import viwid.layout
import viwid.event.input

import curses


class _Property(property):

    def __init__(self, setter, default=lambda: None):
        super().__init__(self._fget, self._fset)
        self.__setter = setter
        self.__name = setter.__name__
        self.__default = default

    def _fget(self, obj):
        return obj._Widget__kwargs.get(self.__name, self.__default())#TODO nicer?!

    def _fset(self, obj, value):
        obj._Widget__kwargs[self.__name] = value
        if obj._Widget__screen:
            self.__setter(obj, value)
        for func in obj._Widget__property_listeners.get(self.__name, ()):
            func()


def Property(setter=None, /, *, default=lambda: None):
    if setter:
        return _Property(setter)
    else:
        def f(seta):
            return _Property(seta, default=default)
        return f


class _ListProperty(property):

    def __init__(self, setter, item_added_func, item_removed_func, item_replaced_func=None):
        super().__init__(self._fget, self._fset)
        self.__item_added_func = item_added_func
        self.__item_removed_func = item_removed_func
        self.__item_replaced_func = item_replaced_func
        self.__name = setter.__name__

    def _fget(self, obj):
        result = obj._Widget__kwargs.get(self.__name, None )  # TODO nicer?!
        if result is None:
            result = obj._Widget__kwargs[self.__name] = viwid.data.List()

        if not hasattr(result, "gof"):
            result.gof = True
            result._add_observer(
                functools.partial(self.__item_added_func, obj),
                functools.partial(self.__item_removed_func, obj),
                functools.partial(self.__item_replaced_func, obj) if self.__item_replaced_func else None,
            )
        return result

    def _fset(self, obj, value):
        self._fget(obj).update(value)


def ListProperty(item_added_func, item_removed_func, item_replaced_func=None):
    def f(seta):
        return _ListProperty(seta, item_added_func, item_removed_func, item_replaced_func)
    return f


class Alignment(enum.Enum):
    START = enum.auto()
    STOP = enum.auto()
    CENTER = enum.auto()
    FILL = enum.auto()


class Widget:

    Property = Property
    ListProperty = ListProperty

    def __init__(self, **kwargs):
        def islist(k):
            return isinstance( getattr(type(self), k), _ListProperty )
        kwargs = {k: (viwid.data.List(v) if islist(k) else v) for k, v in kwargs.items()}
        self.__kwargs = dict(kwargs or {})
        self.__screen = None
        self.__position = viwid.Point(0, 0)
        self.__offset = viwid.Point(0, 0)
        self.__size = viwid.Size(0, 0)
        self.__inner_size = viwid.Size(0, 0)
        self.__parent = None
        self.__property_listeners = {}
        self.__layout = viwid.layout.NullLayout()
        self.__root_style = None
        self.__compute_width_cache = [None, None]
        self.__compute_height_cache = [None, None]
        self.__foreground = None
        self.__background = None

    @property
    def computed_vertical_expand_greedily(self):
        if self.vertical_expand_greedily is not None:
            return self.vertical_expand_greedily
        for child in getattr(self, "children", ()):
            if child.computed_vertical_expand_greedily:
                return True
        return False

    @property
    def computed_horizontal_expand_greedily(self):
        if self.horizontal_expand_greedily is not None:
            return self.horizontal_expand_greedily
        for child in getattr(self, "children", ()):
            if child.computed_horizontal_expand_greedily:
                return True
        return False

    @property
    def computed_is_disabled(self):
        return self.is_disabled or (self.parent.computed_is_disabled if self.parent else False)

    @Property(default=lambda: False)
    def is_disabled(self, value):
        self.request_repaint()

    @property
    def foreground(self):
        return self.__foreground

    @foreground.setter
    def foreground(self, value):
        self.__foreground = value
        self.request_repaint()

    @property
    def background(self):
        return self.__background

    @background.setter
    def background(self, value):
        self.__background = value
        self.request_repaint()


    @Property
    def vertical_expand_greedily(self, value):
        self.request_resize()

    @Property
    def horizontal_expand_greedily(self, value):
        self.request_resize()

    @Property
    def vertical_alignment(self, value):
        self.request_resize()

    @Property
    def horizontal_alignment(self, value):
        self.request_resize()

    @property
    def root_style(self):
        return self.__root_style or self.parent.root_style

    def set_root_style(self, v):
        self.__root_style = v

    @property
    def class_style_name(self):
        return "plain"

    @property
    def style_atom(self):
        return self.style_atom_by_name(self.class_style_name)

    def style_atom_by_name(self, name):
        class_style = getattr(self.root_style, name)
        if self.computed_is_disabled:
            atom_name = "disabled"
        elif self.screen.focussed_widget is self:
            atom_name = "focussed"
        else:
            atom_name = "normal"
        return getattr(class_style, atom_name)

    @property
    def layout(self):
        return self.__layout

    def set_layout(self, value):
        self.__layout = value
        self.request_resize()

    def listen_property(self, key, func):#TODO remover
        self.__property_listeners[key] = l = self.__property_listeners.get(key) or []
        l.append(func)

    def alive(self):
        w = self
        while w.parent:
            w = w.parent
        #return w.screen and   (w == w.screen.root_widget or w in w.screen.popups)
        #TODO
        return not w.screen or w in w.screen.roots

    def paint2(self, parent_canvas=None):
        if not self.alive():
            return
        if not (self.background or self.style_atom.background) and not parent_canvas:
            return self.parent.paint2()
        canvas = self.canvas()
        if self.background or self.style_atom.background:
            canvas.fill(self.background or self.style_atom.background,
                        viwid.Rectangle(viwid.Point(0, 0), viwid.Point(self.size.width, self.size.height)))
        self.paint(canvas)

    @property
    def focusable(self):
        return False

    class Parti:

        def __init__(self, widget):
            self.__widget = widget

        def focussed(self):
            focu = self.__widget.screen.focussed_widget
            for child in self.__widget._children:
                w = focu
                isit = False
                while w:
                    if w == child:
                        return w
                    w = w.parent

        def jumpto(self, frm, delta):
            dx, dy = delta
            res = None
            dist = sys.maxsize
            if dx:
                px = frm.position.x + (0 if dx<0 else frm.size.width)
                py1 = frm.position.y
                py2 = py1 + frm.size.height
                for chld in self.__widget._children:
                    if chld is frm:
                        continue
                    if dx*chld.position.x >= dx*px and ( (py1 <= chld.position.y < py2) or (py1 <= (chld.position.y+chld.size.height) < py2) ):
                        ddist = abs( chld.position.x - frm.position.x )
                        if ddist < dist:
                            res = chld
                            dist = ddist
            elif dy:
                py = frm.position.y + (0 if dy<0 else frm.size.height)
                px1 = frm.position.x
                px2 = px1 + frm.size.width
                for chld in self.__widget._children:
                    if chld is frm:
                        continue
                    if dy*chld.position.y >= dy*py and ( (px1 <= chld.position.x < px2) or (px1 <= (chld.position.x+chld.size.width) < px2) ):
                        ddist = abs( chld.position.y - frm.position.y )
                        if ddist < dist:
                            res = chld
                            dist = ddist
            return res

    def _keyboard_event(self, event: viwid.event.input.OngoingKeyboardEvent) -> None:
        if self.screen is None:
            return
        focu = self.screen.focussed_widget
        if focu is None:
            return
        delta = (-1 if event.key == curses.KEY_LEFT else 1 if event.key == curses.KEY_RIGHT else 0), (
            -1 if event.key == curses.KEY_UP else 1 if event.key == curses.KEY_DOWN else 0)
        parti = self.Parti(self)
        xxx = parti.focussed()
        while xxx:
            xxx = parti.jumpto(xxx, delta)
            if not xxx:
                return
            if xxx.try_focus():
                event.stop_propagation()
                return

    def _preview_keyboard_event(self, event: viwid.event.input.OngoingKeyboardEvent) -> None:
        pass

    def _internal_mouse_click_event(self, event: viwid.event.input.OngoingMouseClickEvent) -> None:
        if self.focusable:
            self.try_focus()
        self._mouse_click_event(event)

    def _preview_internal_mouse_click_event(self, event: viwid.event.input.OngoingMouseClickEvent) -> None:
        self._preview_mouse_click_event(event)

    def _mouse_click_event(self, event: viwid.event.input.OngoingMouseClickEvent) -> None:
        pass

    def _preview_mouse_click_event(self, event: viwid.event.input.OngoingMouseClickEvent) -> None:
        pass

    def _scroll_event(self, event: viwid.event.input.OngoingScrollEvent) -> None:
        pass

    def _preview_scroll_event(self, event: viwid.event.input.OngoingScrollEvent) -> None:
        pass

    @property
    def parent(self) -> t.Optional["Widget"]:
        return self.__parent

    @property
    def position(self) -> viwid.Point:
        return self.__position

    @property
    def offset(self) -> viwid.Point:
        return self.__offset

    @property
    def size(self) -> viwid.Size:
        return self.__size

    @property
    def inner_size(self) -> viwid.Size:
        return self.__inner_size

    def set_parent(self, value: t.Optional["Widget"]) -> None:
        self.__parent = value

    def set_position(self, value: viwid.Point) -> None:
        self.__position = value

    def set_offset(self, value: viwid.Point) -> None:
        self.__offset = value
        self.request_repaint()

    def set_size(self, value: viwid.Size, setinner=True) -> None:
        self.__size = value
        if setinner:
            self.set_inner_size(value)

    def set_inner_size(self, value: viwid.Size) -> None:
        self.__inner_size = value
        self.__layout.set_size(value)

    def canvas(self):
        return self.screen.driver.canvas(self)

    def child_at_position(self, xx, yy):
        xx -= self.offset.x
        yy -= self.offset.y
        for child in self._children:
            if child.position.x <= xx and child.position.y <= yy and (xx < child.position.x+child.size.width) and (yy < child.position.y+child.size.height):
                return child.child_at_position(xx-child.position.x, yy-child.position.y)
        return self #TODO

    @property
    def screen(self) -> "viwid.screen.Screen":
        return self.__screen

    def try_focus(self):
        if self.focusable and self.screen:
            self.screen.focussed_widget = self
            return True
        for child in self._children:
            if child.try_focus():
                return True

    def compute_width2(self, minimal: bool) -> int:
        result = self.__compute_width_cache[int(minimal)]
        if result is None:
            result = self.__compute_width_cache[int(minimal)] = self.compute_width(minimal)
        return result

    def compute_height2(self, width: int, minimal: bool) -> int:
        result = self.__compute_height_cache[int(minimal)]
        if (result is None) or (result[0] != width):
            result = self.__compute_height_cache[int(minimal)] = width, self.compute_height(width, minimal)
        return result[1]

    def compute_width(self, minimal: bool) -> int:
        return self.__layout.compute_width(minimal)

    def compute_height(self, width: int, minimal: bool) -> int:
        return self.__layout.compute_height(width, minimal)

    def request_repaint(self) -> None:
        if self.screen:
            self.screen.driver.repaint_widget_soon(self)

    def request_resize(self) -> None:
        self.__compute_width_cache = [None, None]
        self.__compute_height_cache = [None, None]
        if self.parent:
            self.parent.request_resize()
        elif self.screen:
            self.screen.driver.resize_widget_soon(self)

    def paint(self, canvas):
        for child in self._children:
            child.paint2(canvas)

    def on_materialized(self) -> None:
        pass

    def on_dematerialized(self) -> None:
        pass

    def materialize(self, screen) -> None:
        if self.__screen:
            return #TODO  raise Exception("...")
        self.__screen = screen
        if self.__kwargs is not None:
            for k, v in list(self.__kwargs.items()):
                setattr(self, k, v)
        self.on_materialized()
        for child in self._children:
            child.materialize(self.screen)
            if self.screen and not self.screen.focussed_widget and child.focusable:
                self.screen.focussed_widget = child

    def dematerialize(self) -> None:
        self.on_dematerialized()
        self.__screen = None

    def __item_added(self, index: int, item: object) -> None:
        item.set_parent(self)
        if self.screen:
            item.materialize(self.screen)
        self.request_resize()

    def __item_removed(self, index: int) -> None:
        self.request_resize()

    @ListProperty(__item_added, __item_removed)
    def _children(self) -> list:
        ...
