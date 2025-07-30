#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import abc
import curses
import typing as t
import viwid.widgets.widget
import viwid.canvas
import viwid.style
import viwid.event.base
import viwid.event.input
import viwid.drivers.driver
import viwid.widgets.box


class Screen:

    def __init__(self, driver: "viwid.drivers.driver.Driver"):
        self.__driver = driver
        self.__style = viwid.style.DEFAULT_STYLE
        self.__roots: list[tuple[viwid.widgets.widget.Widget, viwid.screen.RootAlignment]] = []

    @property
    def style(self) -> viwid.style.Style:
        return self.__style

    @property
    def driver(self):
        return self.__driver

    def add_root(self, widget: viwid.widgets.widget.Widget,
                 alignment: t.Optional["RootAlignment"] = None, *, root_style_name: str = "main") -> "TODO":
        if not alignment:
            alignment = RootAlignment(
                FixedRootAlignmentPositioning(x=0),
                FixedRootAlignmentPositioning(y=0),
                ByScreenRootAlignmentSizing(width_fraction=1),
                ByScreenRootAlignmentSizing(height_fraction=1))
        rootroot = viwid.widgets.box.CBox(children=[widget])
        rootroot.set_root_style(getattr(self.style, root_style_name))
        self.__roots.append(tp := (rootroot, alignment))
        rootroot.materialize(self)
        alignment.apply(rootroot)
        self.update()
        def rm():
            self.__roots.remove(tp)
            self.update()
        return rm

    def popup(self, widget: viwid.widgets.widget.Widget,
              alignment: t.Optional["RootAlignment"] = None, *, root_style_name: str = "popup") -> "TODO":
        if not alignment:
            alignment = RootAlignment(
                CenterRootAlignmentPositioning(),
                CenterRootAlignmentPositioning(),
                AutoRootAlignmentSizing(),
                AutoRootAlignmentSizing())
        rm = self.add_root(widget, alignment=alignment, root_style_name=root_style_name)
        self.focussed_widget = None
        widget.try_focus()
        return rm

    def update(self) -> None:
        for popup, alignment in self.__roots:
            popup.paint2()

    @property
    def roots(self) -> t.Iterable[viwid.widgets.widget.Widget]:
        return tuple([x[0] for x in self.__roots])

    @property
    def roots_and_alignments(self) -> t.Iterable[tuple[viwid.widgets.widget.Widget, "RootAlignment"]]:
        return tuple(self.__roots)

    @property
    @abc.abstractmethod
    def size(self) -> viwid.Size:
        pass

    @property
    def topmost(self) -> t.Optional[viwid.widgets.widget.Widget]:
        return self.__roots[-1][0] if self.__roots else None

    @property
    def bottommost(self) -> t.Optional[viwid.widgets.widget.Widget]:
        return self.__roots[0][0] if self.__roots else None

    @property
    @abc.abstractmethod
    def focussed_widget(self) -> t.Optional[viwid.widgets.widget.Widget]:
        pass

    @focussed_widget.setter
    @abc.abstractmethod
    def focussed_widget(self, value):
        pass

    @staticmethod
    def handle_event(widget: "viwid.widgets.widget.Widget", ongoing_event: viwid.event.base.OngoingEvent) -> None:
        if isinstance(ongoing_event, viwid.event.input.OngoingKeyboardEvent) and ongoing_event.key in [9,curses.KEY_BTAB]:
            Screen.__handle_event__tab_key(widget, ongoing_event.key == curses.KEY_BTAB)

        else:
            pth = []
            fw = widget
            while fw:
                pth.append(fw)
                fw = fw.parent
            for pt in reversed(pth):
                if not pt.computed_is_disabled:
                    getattr(pt, f"_preview_{ongoing_event.name}_event")(ongoing_event)
            w = widget
            while w and not ongoing_event.is_propagation_stopped:
                if not w.computed_is_disabled:
                    getattr(w, f"_{ongoing_event.name}_event")(ongoing_event)
                w = w.parent

    @staticmethod
    def __handle_event__tab_key(widget: "viwid.widgets.widget.Widget", reverse: bool) -> None:
        def widgets_flat(W):
            for wc in W._children:
                for xxx in widgets_flat(wc):
                    yield xxx
            yield W

        def _all_screen_widgets():
            for root_widget in widget.screen.roots:
                for wl in widgets_flat(root_widget):
                    yield wl

        all_screen_widgets = _all_screen_widgets()

        if reverse:
            all_screen_widgets = reversed(list(all_screen_widgets))

        ww = None
        for w in all_screen_widgets:
            if ww:
                if w.focusable and w.try_focus():
                    return
            elif w is widget:
                ww = w

    def translate_coordinates_with_visibility_check(self, point: viwid.Point, *,
                                                    old_origin: t.Optional[viwid.widgets.widget.Widget] = None,
                                                    new_origin: t.Optional[viwid.widgets.widget.Widget] = None
                                                    ) -> tuple[viwid.Point, bool]:
        is_visible = "TODO"
        while old_origin is not None:
            if point.x+old_origin.offset.x < 0 or point.y+old_origin.offset.y < 0 or \
                    point.x+old_origin.offset.x >= old_origin.size.width or point.y+old_origin.offset.y >= old_origin.size.height:
                is_visible = False
            point += old_origin.position + old_origin.offset
            old_origin = old_origin.parent
        if new_origin is not None:
            reverse_point, reverse_is_visible = self.translate_coordinates_with_visibility_check(viwid.Point(0, 0),
                                                                                                 old_origin=new_origin,
                                                                                                 new_origin=None)
            point -= reverse_point
            #is_visible = is_visible and reverse_is_visible
        return point, is_visible

    def translate_coordinates(self, point: viwid.Point, *, old_origin: t.Optional[viwid.widgets.widget.Widget] = None,
                              new_origin: t.Optional[viwid.widgets.widget.Widget] = None) -> viwid.Point:
        return self.translate_coordinates_with_visibility_check(point, old_origin=old_origin, new_origin=new_origin)[0]


class RootAlignmentPositioning(abc.ABC):

    @abc.abstractmethod
    def get_x(self, widget: viwid.widgets.widget.Widget, screen_size: viwid.Size) -> int:
        pass

    @abc.abstractmethod
    def get_y(self, widget: viwid.widgets.widget.Widget, screen_size: viwid.Size) -> int:
        pass


class AnchorRootAlignmentPositioning(RootAlignmentPositioning):

    def __init__(self, anchor_widget: viwid.widgets.widget.Widget):
        self.__anchor_widget = anchor_widget

    def get_x(self, widget, screen_size):
        widget_screen_position = self.__anchor_widget.screen.translate_coordinates(viwid.Point(0, 0), old_origin=self.__anchor_widget)
        return max(0, min(widget_screen_position.x, screen_size.width-widget.size.width))

    def get_y(self, widget, screen_size):
        widget_screen_position = self.__anchor_widget.screen.translate_coordinates(viwid.Point(0, 0), old_origin=self.__anchor_widget)
        if (widget_screen_position.y + self.__anchor_widget.size.height + widget.size.height) <= screen_size.height:
            return widget_screen_position.y + self.__anchor_widget.size.height
        if widget_screen_position.y >= widget.size.height:
            return widget_screen_position.y - widget.size.height
        return max(0, screen_size.height-widget.size.height)


class CenterRootAlignmentPositioning(RootAlignmentPositioning):

    def get_x(self, widget, screen_size):
        gapx = screen_size.width - widget.size.width
        gapx = max(0, gapx)
        return int(gapx/2)

    def get_y(self, widget, screen_size):
        gapy = screen_size.height - widget.size.height
        gapy = max(0, gapy)
        return int(gapy/2)


class FixedRootAlignmentPositioning(RootAlignmentPositioning):

    def __init__(self, x=0, y=0):
        self.__x = x
        self.__y = y

    def get_x(self, widget, screen_size):
        return self.__x

    def get_y(self, widget, screen_size):
        return self.__y


class RootAlignmentSizing(abc.ABC):

    @abc.abstractmethod
    def get_width(self, widget: viwid.widgets.widget.Widget, screen_size: viwid.Size) -> int:
        pass

    @abc.abstractmethod
    def get_height(self, width: int, widget: viwid.widgets.widget.Widget, screen_size: viwid.Size) -> int:
        pass


class AutoRootAlignmentSizing(RootAlignmentSizing):

    def __init__(self, minimal_width=False, minimal_height=False):
        self.__minimal_width = minimal_width
        self.__minimal_height = minimal_height

    def get_width(self, widget, screen_size):
        width = widget.compute_width2(minimal=self.__minimal_width)
        width = min(screen_size.width, width)
        return width

    def get_height(self, width, widget, screen_size):
        height = widget.compute_height2(width, minimal=self.__minimal_height)
        height = min(screen_size.height, height)
        return height


class FixedRootAlignmentSizing(RootAlignmentSizing):

    def __init__(self, width=1, height=1):
        self.__width = width
        self.__height = height

    def get_width(self, widget, screen_size):
        return self.__width

    def get_height(self, width, widget, screen_size):
        return self.__height


class ByScreenRootAlignmentSizing(RootAlignmentSizing):

    def __init__(self, width_fraction=0.5, height_fraction=0.5):
        self.__width_fraction = width_fraction
        self.__height_fraction = height_fraction

    def get_width(self, widget, screen_size):
        return int(screen_size.width * self.__width_fraction)

    def get_height(self, width, widget, screen_size):
        return int(screen_size.height * self.__height_fraction)


class RootAlignment:

    def __init__(self, horizontal_positioning, vertical_positioning, horizontal_sizing, vertical_sizing):
        self.__horizontal_sizing = horizontal_sizing
        self.__horizontal_positioning = horizontal_positioning
        self.__vertical_sizing = vertical_sizing
        self.__vertical_positioning = vertical_positioning

    def apply(self, widget: viwid.widgets.widget.Widget):
        screen_size = widget.screen.size
        width = self.__horizontal_sizing.get_width(widget, screen_size)
        height = self.__vertical_sizing.get_height(width, widget, screen_size)
        widget.set_size(viwid.Size(width, height))
        x = self.__horizontal_positioning.get_x(widget, screen_size)
        y = self.__vertical_positioning.get_y(widget, screen_size)
        widget.set_position(viwid.Point(x, y))
