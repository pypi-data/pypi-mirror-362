# SPDX-FileCopyrightText: © 2025 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only
"""
See :py:class:`LocationBar`.
"""
import typing as t

import klovve


class LocationBar[T](klovve.ui.Piece):
    """
    A horizontal bar that shows a path-like location by its path segments, allowing the user to choose one of them (e.g.
    in order to navigate to these ancestor locations).
    """

    #: The location segments.
    segments: list[T] = klovve.ui.list_property()

    #: The function that translates segments to their textual representation.
    segment_label_func: t.Callable[[T], str] = klovve.ui.property(initial=lambda: str)

    vertical_layout = klovve.ui.property(initial=klovve.ui.Layout(klovve.ui.Align.START))

    def _segment_selected(self, segment: T) -> None:
        self.trigger_event(LocationBar.LocationSelectedEvent(self, segment))

    class LocationSelectedEvent(klovve.event.Event):
        """
        Event that occurs when the user 'clicks' on a segment in a :py:class:`LocationBar`.
        """

        def __init__(self, location_bar: "LocationBar[T]", segment: T):
            super().__init__()
            self.__location_bar = location_bar
            self.__segment = segment

        @property
        def location_bar(self) -> "LocationBar[T]":
            """
            The location bar.
            """
            return self.__location_bar

        @property
        def segment(self) -> T:
            """
            The selected segment.
            """
            return self.__segment
