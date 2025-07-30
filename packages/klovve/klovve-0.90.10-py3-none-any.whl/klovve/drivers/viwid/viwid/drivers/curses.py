#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import dataclasses
import enum
import viwid.drivers.driver
import viwid.canvas
import viwid.loop
import viwid.screen
import viwid.widgets.box
import viwid.widgets.widget
import viwid.widgets.label
import viwid.event.input

import asyncio
import curses
import typing as t


class Driver(viwid.drivers.driver.Driver):

    def __init__(self, event_loop):
        self.__curses_colors = _CursesColors()
        self.__screens: list[viwid.screen.Screen] = []
        self.__loop = _Loop(event_loop, self)
        self.__curses_screen = curses.initscr()
        self.__curses_screen.keypad(True)
        curses.curs_set(0)
        curses.noecho()
        self.__curses_screen.clear()
        curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
        curses.flushinp()
        curses.noecho()
        try:
            curses.start_color()
        except:
            pass
        curses.cbreak()
        # TODO curses.wrapper
        self.__curses_screen.nodelay(True)
        self.__requests = None

    def add_widget_screen(self, widget):
        # noinspection PyTypeChecker
        new_screen = _Screen(self.__curses_screen, self)
        new_screen.add_root(widget)
        self.__screens.append(new_screen)
        return new_screen

    @property
    def loop(self):
        return self.__loop

    @property
    def screens(self):
        return tuple(self.__screens)

    @property
    def curses_colors(self):
        return self.__curses_colors

    def repaint_widget_soon(self, widget):
        self.__requests_queue().append(("rep", widget))

    def resize_widget_soon(self, widget):
        self.__requests_queue().append(("res", widget))

    def canvas(self, widget):
        # noinspection PyTypeChecker
        return _Canvas(self, self.__curses_screen, widget)

    def refresh_curses_window(self):
        self.__curses_screen.refresh()

    def process_curses_input(self):
        key = self.__curses_screen.getch()
        if key != curses.ERR:
            if key == curses.KEY_MOUSE:
                curses_mouse_event = curses.getmouse()
                if curses_mouse_event:
                    event_screen_position = viwid.Point(curses_mouse_event[1], curses_mouse_event[2])
                    wheel_up = bool(curses_mouse_event[4] & curses.BUTTON1_PRESSED << (5 - 1) * 5)
                    wheel_down = bool(curses_mouse_event[4] & 65536)
                    for screen in self.screens:  # TODO only active
                        fug = event_screen_position - screen.topmost.position
                        widget = screen.topmost.child_at_position(fug.x, fug.y)
                        if widget:
                            if wheel_up or wheel_down:
                                ongoing_event = viwid.event.input.OngoingScrollEvent(event_screen_position,
                                                                                     direction=1 if wheel_down else -1)
                            else:
                                ongoing_event = viwid.event.input.OngoingMouseClickEvent(
                                    event_screen_position,
                                    left_button=bool(curses_mouse_event[4] & curses.BUTTON1_CLICKED),
                                    right_button=bool(curses_mouse_event[4] & curses.BUTTON3_CLICKED))
                            screen.handle_event(widget, ongoing_event)
            elif key == curses.KEY_RESIZE:
                for screen in self.__screens:  # TODO only active
                    screen.update_curses_screensize()
            else:
                for screen in self.__screens:  # TODO only active
                    if screen.focussed_widget:
                        ongoing_event = viwid.event.input.OngoingKeyboardEvent(key)
                        screen.handle_event(screen.focussed_widget, ongoing_event)
                    elif screen.topmost:
                        screen.topmost.try_focus()
            return True

    def __requests_queue(self):
        def _do_requests():
            has_resize = any([x[0]=="res" for x in self.__requests])
            # TODO stuss
            if has_resize:
                for screen in self.__screens:
                    screen.update_curses_screensize()
            else:
                for req, wid in self.__requests:
                    if req == "rep":
                        wid.paint2()
                    else:
                        raise Exception("TODO")
            self.__curses_screen.refresh()
            self.__requests = None
        if self.__requests is None:
            try:
                asyncio.get_running_loop().call_soon(_do_requests)
                self.__requests = []
            except:
                return []  # TODO
        return self.__requests


class _Loop(viwid.loop.Loop):

    def __init__(self, event_loop, driver: Driver):
        super().__init__(event_loop)
        self.__driver = driver

    async def run(self) -> None:
        for screen in self.__driver.screens:
            screen.update()
            self.__driver.refresh_curses_window()
        while True:
            while True:
                if not self.__driver.process_curses_input():
                    break
            await asyncio.sleep(0.1)


class _Screen(viwid.screen.Screen):

    def __init__(self, curses_screen: curses.window, driver: Driver):
        super().__init__(driver)
        self.__curses_screen = curses_screen
        self.__size = None
        self.update_curses_screensize()
        self.__fowi = None
        self.add_root(viwid.widgets.label.Label())

    def update_curses_screensize(self):
        sh, sw = self.__curses_screen.getmaxyx()
        self.__size = viwid.Size(sw, sh)
        for root, alignment in self.roots_and_alignments:
            alignment.apply(root)
        self.update()

    @property
    def size(self) -> viwid.Size:
        return self.__size

    @property
    def focussed_widget(self):
        if self.__fowi and not self.__fowi.alive():
            self.__fowi = None
        return self.__fowi

    @focussed_widget.setter
    def focussed_widget(self, value):
        old = self.__fowi
        self.__fowi = value
        if value:
            value.request_repaint()
        if old:
            old.request_repaint()


class _Canvas(viwid.canvas.Canvas):

    def __init__(self, driver: Driver, window: curses.window, widget: viwid.widgets.widget.Widget):
        super().__init__()
        self.__driver = driver
        self.__window = window
        self.__widget = widget

    def fill(self, color, rectangle=None):
        if rectangle is None:
            rectangle = viwid.Rectangle(viwid.Point(0, 0), self.__widget.size)
        color = self.FullColor.from_string(color)
        if color.rich.a == 1:
            self.__window.attron(curses.color_pair(self.__driver.curses_colors.color_pair(viwid.canvas.Color(0, 0, 0),
                                                                                          color.base)))
            for ay in range(rectangle.height):
                for ax in range(rectangle.width):
                    op = rectangle.top_left.moved_by(ax, ay)
                    p, isv = self.__widget.screen.translate_coordinates_with_visibility_check(op,
                                                                                              old_origin=self.__widget)
                    if isv:
                        try:
                            # noinspection PyArgumentList
                            self.__window.addstr(p.y, p.x, " ")
                        except: pass

    def text(self, text, rectangle=None):
        if rectangle is None:
            rectangle = viwid.Rectangle(viwid.Point(0, 0), self.__widget.size)
        widg = self.__widget
        fg = None
        while widg and (fg is None):
            fg = widg.foreground or widg.style_atom.foreground
            if fg:
                break
            widg = widg.parent
        fg = self.FullColor.from_string(fg).base
        fgc = fg
        x, y = rectangle.left_x, rectangle.top_y
        for cha in text:
            if cha == "\n":
                x = rectangle.left_x
                y += 1
                continue
            p, isv = self.__widget.screen.translate_coordinates_with_visibility_check(viwid.Point(x, y),
                                                                                      old_origin=self.__widget)
            if isv:
                try:
                 self.__window.move(p.y, p.x)
                except: continue
                ats = self.__window.inch()
                pair = ats >> 8
                _, bgc = self.__driver.curses_colors.colors_by_pair(pair)
                self.__window.addstr(cha, curses.color_pair(self.__driver.curses_colors.color_pair(fgc, bgc)))
            x += 1

    def cursor(self, point):
        p, isv = self.__widget.screen.translate_coordinates_with_visibility_check(viwid.Point(point.x, point.y),
                                                                                  old_origin=self.__widget)
        if isv:
            if self.__widget is self.__widget.screen.focussed_widget:
                # noinspection PyArgumentList
                self.__window.chgat(p.y, p.x, 1, curses.color_pair(self.__driver.curses_colors.color_pair(
                    self.Color(0, 0, 0), self.Color(1, 1, 0))))


class _CursesColors:

    curses_colors = [curses.COLOR_BLACK, curses.COLOR_BLUE, curses.COLOR_GREEN, curses.COLOR_CYAN,
                     curses.COLOR_RED, curses.COLOR_MAGENTA, curses.COLOR_YELLOW, curses.COLOR_WHITE]

    class Mode(enum.Enum):
        COLORS_8 = enum.auto()
        COLORS_256 = enum.auto()

    def __init__(self):
        self.__mode = _CursesColors.Mode.COLORS_8
        self.__curses_colors = {}
        self.__curses_color_pairs = {}
        self.__next_color_number = 100
        self.__next_color_pair_number = 50

    def __curses_color(self, color: viwid.canvas.Color):
        if self.__mode == _CursesColors.Mode.COLORS_256:
            color_tuple = (int(color.r * 1000), int(color.g * 1000), int(color.b * 1000))
            result = self.__curses_colors.get(color_tuple)
            if result is None:
                curses.init_color(self.__next_color_number, *color_tuple)
                result = self.__curses_colors[color_tuple] = self.__next_color_number
                self.__next_color_number += 1
        else:
            return _CursesColors.curses_colors[(1 if color.b >= 0.5 else 0) + (2 if color.g >= 0.5 else 0)
                                               + (4 if color.r >= 0.5 else 0)]
        return result

    def color_pair(self, fg: t.Union[viwid.canvas.FullColor, viwid.canvas.Color, str],
                   bg: t.Union[viwid.canvas.FullColor, viwid.canvas.Color, str]):
        if isinstance(fg, int):
            fg_color_number = fg
        else:
            fg = viwid.canvas.FullColor.from_string(fg)
            fg_color_number = self.__curses_color(fg.base)
        if isinstance(bg, int):
            bg_color_number = bg
        else:
            bg = viwid.canvas.FullColor.from_string(bg)
            bg_color_number = self.__curses_color(bg.base)
        pair_tuple = fg_color_number, bg_color_number
        result = self.__curses_color_pairs.get(pair_tuple)
        if result is None:
            curses.init_pair(self.__next_color_pair_number, *pair_tuple)
            result = self.__curses_color_pairs[pair_tuple] = self.__next_color_pair_number
            self.__next_color_pair_number += 1
        return result

    def colors_by_pair(self, pair):
        for n, p in self.__curses_color_pairs.items():
            if p == pair:
                return n
