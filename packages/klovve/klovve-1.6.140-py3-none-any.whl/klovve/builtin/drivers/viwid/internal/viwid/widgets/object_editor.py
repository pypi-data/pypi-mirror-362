# SPDX-FileCopyrightText: © 2025 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only
"""
See :py:class:`ObjectEditor`.
"""
import viwid.widgets
import viwid.styling
from viwid.widgets.widget import Widget as _Widget


class ObjectEditor(_Widget):
    """
    An object editor.

    This is a complex widget that allows the user to inspect and edit a tree-like structure of objects.
    """

    def __init__(self, **kwargs):
        self.__remove_button = viwid.widgets.button.Button(
            text="X", decoration=viwid.widgets.button.Decoration.NONE)
        self.__header_bar_expanded = viwid.widgets.box.Box()
        self.__header_button_collapsed = viwid.widgets.button.Button(
            margin=viwid.Margin(bottom=1),
            decoration=viwid.widgets.button.Decoration.NONE,
            horizontal_alignment = viwid.Alignment.FILL_EXPANDING)  #  TODO should be only FILL?!
        self.__header_button_expanded = viwid.widgets.button.Button(
            decoration=viwid.widgets.button.Decoration.NONE,
            horizontal_alignment=viwid.Alignment.FILL_EXPANDING)  #  TODO should be only FILL?!
        self.__actions_box = viwid.widgets.box.Box(orientation=viwid.Orientation.VERTICAL,
                                                   horizontal_alignment=viwid.Alignment.END)
        self.__outer_box = viwid.widgets.box.Box(orientation=viwid.Orientation.VERTICAL, margin=viwid.Margin(bottom=1))
        self.__inner_box = viwid.widgets.box.Box(orientation=viwid.Orientation.VERTICAL)
        self.__inner_box.children.append(inner_head_box := viwid.widgets.box.Box(
            orientation=viwid.Orientation.VERTICAL, horizontal_alignment=viwid.Alignment.END))
        self.__property_grid = ObjectEditor._PropertyGrid()
        self.__inner_box.children.append(self.__property_grid)
        self.__additional_widgets_box = viwid.widgets.box.Box(orientation=viwid.Orientation.VERTICAL,
                                                              horizontal_alignment=viwid.Alignment.END)
        self.__border_box_right = viwid.widgets.box.Box(minimal_size=viwid.Size(1, 1),
                                                        horizontal_alignment=viwid.Alignment.FILL)
        self.__border_box_left = viwid.widgets.box.Box(minimal_size=viwid.Size(1, 1),
                                                       horizontal_alignment=viwid.Alignment.FILL)
        self.__border_box_bottom = viwid.widgets.box.Box(minimal_size=viwid.Size(1, 1),
                                                         vertical_alignment=viwid.Alignment.FILL)
        self.__border_box = viwid.widgets.box.Box(
            orientation=viwid.Orientation.VERTICAL,
            children=(
                viwid.widgets.box.Box(
                    orientation=viwid.Orientation.HORIZONTAL,
                    children=(self.__border_box_right, self.__inner_box, self.__border_box_left)),
                self.__border_box_bottom))

        super().__init__(**{**dict(layout=viwid.layout.GridLayout(viwid.layout.GridLayout.VERTICAL_PARTITIONER,)),
                            **kwargs})

        self.__outer_box.children.append(self.__header_bar_expanded)
        self.__header_bar_expanded.children.append(self.__header_button_expanded)
        self.__outer_box.children.append(self.__border_box)
        self.__header_bar_expanded.children.append(self.__remove_button)
        inner_head_box.children.append(self.__actions_box)
        inner_head_box.children.append(self.__additional_widgets_box)

    def _materialize(self):
        super()._materialize()

        self.__header_button_collapsed.listen_event(viwid.widgets.button.Button.TriggeredEvent,
                                                    self.__handle_toggle_expand_clicked)
        self.__header_button_expanded.listen_event(viwid.widgets.button.Button.TriggeredEvent,
                                                   self.__handle_toggle_expand_clicked)
        self.__remove_button.listen_event(viwid.widgets.button.Button.TriggeredEvent,
                                          self.__handle_remove_button_clicked)
        self.__actions_box.listen_event(viwid.widgets.button.Button.TriggeredEvent,
                                        self.__handle_action_button_clicked)

    def _dematerialize(self):
        self.__header_button_collapsed.unlisten_event(self.__handle_toggle_expand_clicked)
        self.__header_button_expanded.unlisten_event(self.__handle_toggle_expand_clicked)
        self.__remove_button.unlisten_event(self.__handle_remove_button_clicked)
        self.__actions_box.unlisten_event(self.__handle_action_button_clicked)

        super()._dematerialize()

    title: str
    @_Widget.Property(default=lambda: "")
    def title(self, _):
        """
        The title text.
        """
        for node_header in (self.__header_button_collapsed, self.__header_button_expanded):
            node_header.text = _

    color: viwid.TColorInput
    @_Widget.Property(default=lambda: "#888")
    def color(self, _):
        """
        The color.
        """
        for side_border_box in (self.__border_box_right, self.__border_box_left, self.__border_box_bottom):
            side_border_box.background = _
        default_button_style = self.layer_style.control
        for button in (self.__header_button_collapsed, self.__header_button_expanded, self.__remove_button):
            button._set_class_style(viwid.styling.Theme.Layer.Class(
                normal=viwid.styling.Theme.Layer.Class.Style(
                    foreground=default_button_style.normal.foreground, background=_),
                hovered=default_button_style.hovered,
                focused=default_button_style.focused,
                activated=default_button_style.activated,
                disabled=default_button_style.disabled))

    is_removable_by_user: bool
    @_Widget.Property(default=lambda: False)
    def is_removable_by_user(self, _):
        """
        Whether this object is removable by the user.
        """
        self.__remove_button.is_visible = _

    is_expanded: bool
    @_Widget.Property(default=lambda: True)
    def is_expanded(self, _):
        """
        Whether this object editor is expanded.
        """
        self._children = (self.__outer_box if _ else self.__header_button_collapsed,)

    def __action_added(self, index: int, item: tuple[str, str]) -> None:
        label, action_name = item
        action_button = viwid.widgets.button.Button(text=label, action=action_name,
                                                    horizontal_alignment=viwid.Alignment.END)
        self.__actions_box.children.insert(index, action_button)

    def __action_removed(self, index: int, item: tuple[str, str]) -> None:
        self.__actions_box.children.pop(index)

    @_Widget.ListProperty(__action_added, __action_removed)
    def actions(self) -> list[tuple[str, str]]:
        """
        The object actions.

        Each is a tuple of the label text and the action name.
        """

    def __property_slot_added(self, index: int, item: tuple[str, "ObjectPropertyEditor"]) -> None:
        label, object_property_editor = item
        inner_index = index * 2

        label_box = viwid.widgets.box.Box(
            children=[
                viwid.widgets.label.Label(
                    text=f"{label}:" if label else "",
                    horizontal_alignment=viwid.Alignment.FILL_EXPANDING,
                    vertical_alignment=viwid.Alignment.START,
                    margin=viwid.Margin(top=1, right=1)),
                viwid.widgets.box.Box(
                    horizontal_alignment=viwid.Alignment.END,
                    minimal_size=viwid.Size(1, 1),
                    background="#BBB",
                    margin=viwid.Margin(top=1, right=1))],
            horizontal_alignment=viwid.Alignment.FILL)

        object_property_editor_box = viwid.widgets.box.Box(
            children=[object_property_editor],
            margin=viwid.Margin(top=1))

        self.__property_grid._children.insert(inner_index, object_property_editor_box)
        self.__property_grid._children.insert(inner_index, label_box)

    def __property_slot_removed(self, index: int, item: tuple[str, "ObjectPropertyEditor"]) -> None:
        inner_index = index * 2
        for _ in range(2):
            self.__property_grid._children.pop(inner_index)

    @_Widget.ListProperty(__property_slot_added, __property_slot_removed)
    def property_slots(self) -> list[tuple[str, "ObjectPropertyEditor"]]:
        """
        The property slots.

        Each is a tuple of the property label text and the object property editor.
        """

    def __additional_widget_added(self, index: int, item: _Widget) -> None:
        self.__additional_widgets_box.children.insert(index, item)

    def __additional_widget_removed(self, index: int, item: _Widget) -> None:
        self.__additional_widgets_box.children.pop(index)

    @_Widget.ListProperty(__additional_widget_added, __additional_widget_removed)
    def additional_widgets(self) -> list[_Widget]:
        """
        The additional widgets to show.
        """

    def __handle_remove_button_clicked(self, event: "viwid.widgets.button.Button.TriggeredEvent"):
        self.screen_layer.trigger_event(self, ObjectEditor.RemoveRequestedEvent())
        event.stop_handling()

    def __handle_action_button_clicked(self, event: "viwid.widgets.button.Button.TriggeredEvent"):
        self.screen_layer.trigger_event(self, ObjectEditor.ExecuteActionRequestedEvent(event.action))
        event.stop_handling()

    def __handle_toggle_expand_clicked(self, event: "viwid.widgets.button.Button.TriggeredEvent"):
        self.is_expanded = not self.is_expanded
        event.stop_handling()

    class _PropertyGrid(_Widget):

        def __init__(self, **kwargs):
            super().__init__(**{**dict(layout=viwid.layout.GridLayout(self.__partitioner)), **kwargs})

        def __partitioner(self, children):
            result = []
            while len(children) > 0:
                result.append(children[:2])
                children = children[2:]
            return result

    class RemoveRequestedEvent(viwid.event.Event):
        """
        Event that occurs when the user requests to remove this object.
        """

    class ExecuteActionRequestedEvent(viwid.event.Event):
        """
        Event that occurs when the user requests to execute an action on this object.
        """

        def __init__(self, action_name: str):
            """
            :param action_name: The action name.
            """
            super().__init__()
            self.__action_name = action_name

        @property
        def action_name(self) -> str:
            """
            The action name.
            """
            return self.__action_name


class ObjectPropertyEditor(_Widget):
    """
    An object property editor.

    Usually used inside an :py:class:`ObjectEditor`.
    """

    def __init__(self, **kwargs):
        self.__add_child_button = viwid.widgets.button.Button(text="+", margin=viwid.Margin(bottom=1, right=1),
                                                              horizontal_alignment=viwid.Alignment.FILL)

        super().__init__(**{**dict(layout=viwid.layout.GridLayout(viwid.layout.GridLayout.VERTICAL_PARTITIONER,)),
                            **kwargs})

        self.__child_object_editors_box = viwid.widgets.box.Box(orientation=viwid.Orientation.VERTICAL,
                                                                margin=viwid.Margin(right=1))
        self._children.append(self.__child_object_editors_box)
        self._children.append(self.__add_child_button)

    children_can_be_added_by_user: bool
    @_Widget.Property(default=lambda: False)
    def children_can_be_added_by_user(self, _):
        """
        Whether children can be added by the user.
        """
        self.__add_child_button.is_visible = _

    def __object_editor_added(self, index: int, item: ObjectEditor) -> None:
        self.__child_object_editors_box.children.insert(index, item)

    def __object_editor_removed(self, index: int, item: ObjectEditor) -> None:
        self.__child_object_editors_box.children.pop(index)

    @_Widget.ListProperty(__object_editor_added, __object_editor_removed)
    def object_editors(self) -> list[ObjectEditor]:
        """
        The children's object editors.
        """

    def _materialize(self):
        super()._materialize()

        self.__add_child_button.listen_event(viwid.widgets.button.Button.TriggeredEvent,
                                             self.__handle_add_child_button_clicked)

    def _dematerialize(self):
        self.__add_child_button.unlisten_event(self.__handle_add_child_button_clicked)

        super()._dematerialize()

    def __handle_add_child_button_clicked(self, event: "viwid.widgets.button.Button.TriggeredEvent") -> None:
        self.screen_layer.trigger_event(self, ObjectPropertyEditor.AddChildRequestedEvent())
        event.stop_handling()

    class AddChildRequestedEvent(viwid.event.Event):
        """
        Event that occurs when the user requests to add a child.
        """
