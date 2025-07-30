# SPDX-FileCopyrightText: © 2025 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only
"""
See :py:class:`ObjectEditor`.
"""
import enum

import klovve.app
from klovve.builtin.views.location_bar import LocationBar as _LocationBar


class ObjectEditor(klovve.ui.Piece):
    """
    An object editor.

    This is a very complex view that allows the user to inspect and edit tree-like structures of objects in custom ways.

    In most cases you should put the root object editor into an :py:class:`ObjectEditorRoot`.

    When a user triggered an object action (see :py:attr:`actions`), :py:class:`ObjectEditor.ActionTriggeredEvent` will
    be triggered.
    When a user triggers the "remove" button (see :py:attr:`is_removable_by_user`),
    :py:class:`ObjectEditor.RemoveRequestedEvent` will be triggered.
    Both will do nothing by default.
    """

    class Coloration(enum.Enum):
        """
        Editor colorations.
        """

        #: Red.
        RED = enum.auto()
        #: Green.
        GREEN = enum.auto()
        #: Blue.
        BLUE = enum.auto()
        #: Yellow.
        YELLOW = enum.auto()
        #: Magenta.
        MAGENTA = enum.auto()
        #: Cyan.
        CYAN = enum.auto()
        #: Gray.
        GRAY = enum.auto()

    #: The object title text.
    title: str = klovve.ui.property(initial="")
    #: Whether this object editor is currently expanded.
    is_expanded: bool = klovve.ui.property(initial=False)
    #: The properties. This is a list of tuples, each containing the property name and the property editor.
    properties: list[tuple[str, "ObjectPropertyEditor"]] = klovve.ui.list_property()
    #: Actions on this object. This is a list of tuples, each containing the action title and name.
    actions: list[tuple[str, str]] = klovve.ui.list_property()
    #: Whether this object is removable by the user.
    is_removable_by_user: bool = klovve.ui.property(initial=False)
    #: The coloration of this object editor.
    coloration: Coloration = klovve.ui.property(initial=Coloration.GRAY)
    #: Additional views.
    additional_views: list[klovve.ui.View] = klovve.ui.list_property()

    horizontal_layout = klovve.ui.property(initial=klovve.ui.Layout(klovve.ui.Align.START))
    vertical_layout = klovve.ui.property(initial=klovve.ui.Layout(klovve.ui.Align.START))

    class ActionTriggeredEvent(klovve.app.BaseApplication.ActionTriggeredEvent):
        """
        Event that occurs when an object action was triggered. It is essentially a
        :py:class:`klovve.app.BaseApplication.ActionTriggeredEvent`, but with additional properties.
        """

        def __init__(self, object_editor: "ObjectEditor", action_name: str):
            super().__init__(object_editor, action_name)

        @property
        def object_editor(self) -> "ObjectEditor":
            """
            The object editor.
            """
            return self.triggering_view

    class RemoveRequestedEvent(klovve.event.Event):
        """
        Event that occurs when the user has requested to remove an object.
        """

        def __init__(self, object_editor: "ObjectEditor"):
            super().__init__()
            self.__object_editor = object_editor

        @property
        def object_editor(self) -> "ObjectEditor":
            """
            The object editor.
            """
            return self.__object_editor

    def trigger_action(self, action_name: str) -> None:
        self.trigger_event(ObjectEditor.ActionTriggeredEvent(self, action_name))

    def request_remove(self):
        self.trigger_event(ObjectEditor.RemoveRequestedEvent(self))


class ObjectPropertyEditor(klovve.ui.Piece):
    """
    An object property editor.

    Used in a definition of a :py:class:`ObjectEditor`.

    When a user attempts to add a new child, :py:class:`ObjectPropertyEditor.AddChildRequestedEvent` will be triggered.
    This will do nothing by default.
    """

    #: List of child object editors.
    children: list[ObjectEditor] = klovve.ui.list_property()
    #: Whether the user can add new children.
    children_can_be_added_by_user: bool = klovve.ui.property(initial=False)

    horizontal_layout = klovve.ui.property(initial=klovve.ui.Layout(klovve.ui.Align.FILL))
    vertical_layout = klovve.ui.property(initial=klovve.ui.Layout(klovve.ui.Align.CENTER))

    class AddChildRequestedEvent(klovve.event.Event):
        """
        Event that occurs when the user has requested to add a new child.
        """

        def __init__(self, object_property_editor: "ObjectPropertyEditor"):
            super().__init__()
            self.__object_property_editor = object_property_editor

        @property
        def object_property_editor(self) -> "ObjectPropertyEditor":
            """
            The object property editor.
            """
            return self.__object_property_editor

    def request_add_child(self):
        self.trigger_event(ObjectPropertyEditor.AddChildRequestedEvent(self))


class ObjectEditorRoot(klovve.ui.Piece):
    """
    A root view for an :py:class:`ObjectEditor` with built-in scrollability and some comfort features.
    """

    #: The root object editor.
    object_editor: ObjectEditor|None = klovve.ui.property()

    class _LocationBar(klovve.ui.ComposedView):

        segments = klovve.ui.list_property()

        vertical_layout = klovve.ui.property(initial=klovve.ui.Layout(klovve.ui.Align.START))

        location_selected_func = klovve.ui.property(initial=lambda: (lambda *_: None))

        def compose(self):
            return klovve.views.LocationBar(segment_label_func=lambda object_editor: object_editor.title,
                                            segments=self.bind.segments)

        @klovve.event.event_handler
        def __handle_location_selected(self, event: _LocationBar.LocationSelectedEvent) -> None:
            self.location_selected_func(event.segment)
