#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import viwid.event.base


class OngoingKeyboardEvent(viwid.event.base.OngoingEvent):

    def __init__(self, key):
        super().__init__("keyboard")
        self.__key = key

    @property
    def key(self):
        return self.__key


class OngoingMouseClickEvent(viwid.event.base.OngoingEvent):

    def __init__(self, screen_position: viwid.Point, left_button: bool, right_button: bool):
        super().__init__("internal_mouse_click")
        self.__screen_position = screen_position
        self.__left_button = left_button
        self.__right_button = right_button

    @property
    def screen_position(self) -> viwid.Point:
        return self.__screen_position

    @property
    def left_button(self) -> bool:
        return self.__left_button

    @property
    def right_button(self) -> bool:
        return self.__right_button


class OngoingScrollEvent(viwid.event.base.OngoingEvent):

    def __init__(self, screen_position: viwid.Point, direction: int):
        super().__init__("scroll")
        self.__screen_position = screen_position
        self.__direction = direction

    @property
    def screen_position(self) -> viwid.Point:
        return self.__screen_position

    @property
    def direction(self) -> int:
        return self.__direction
