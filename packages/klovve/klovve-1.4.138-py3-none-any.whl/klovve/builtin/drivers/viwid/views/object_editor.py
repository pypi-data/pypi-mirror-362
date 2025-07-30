# SPDX-FileCopyrightText: © 2025 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only
import asyncio
import functools

import viwid.app.screen

import klovve.builtin.drivers.viwid
import klovve.data


class ObjectEditor(klovve.builtin.drivers.viwid.ViewMaterialization[klovve.views.ObjectEditor]):

    def create_native(self):
        viwid_object_editor = self.new_native(
            viwid.widgets.object_editor.ObjectEditor, self.piece, title=self.piece.bind.title,
            color=self.bind.color,
            is_removable_by_user=self.piece.bind.is_removable_by_user, is_expanded=self.piece.bind.is_expanded)

        self.piece._introspect.observe_list_property(
            self.piece._introspect.property_by_name("actions"),
            ObjectEditor._ActionListObserver, (self, viwid_object_editor), owner=self)
        self.piece._introspect.observe_list_property(
            self.piece._introspect.property_by_name("properties"),
            ObjectEditor._PropertyListObserver, (self, viwid_object_editor), owner=self)
        self.piece._introspect.observe_list_property(
            self.piece._introspect.property_by_name("additional_views"),
            ObjectEditor._AdditionalViewsListObserver, (self, viwid_object_editor), owner=self)
        viwid_object_editor.listen_event(viwid.widgets.object_editor.ObjectEditor.RemoveRequestedEvent,
                                         self.__handle_remove_requested)
        viwid_object_editor.listen_event(viwid.widgets.object_editor.ObjectEditor.ExecuteActionRequestedEvent,
                                         self.__handle_execute_action_requested)

        return viwid_object_editor

    def _(self):
        return {
            klovve.views.ObjectEditor.Coloration.RED: "#D33",
            klovve.views.ObjectEditor.Coloration.GREEN: "#3D3",
            klovve.views.ObjectEditor.Coloration.BLUE: "#33D",
            klovve.views.ObjectEditor.Coloration.YELLOW: "#AA3",
            klovve.views.ObjectEditor.Coloration.MAGENTA: "#A3A",
            klovve.views.ObjectEditor.Coloration.CYAN: "#3AA",
        }.get(self.piece.coloration, "#888")
    color: str = klovve.ui.computed_property(_)

    def __handle_remove_requested(self, event: viwid.widgets.object_editor.ObjectEditor.RemoveRequestedEvent) -> None:
        self.piece.request_remove()
        event.stop_handling()

    def __handle_execute_action_requested(
            self, event: viwid.widgets.object_editor.ObjectEditor.ExecuteActionRequestedEvent) -> None:
        self.piece.trigger_action(event.action_name)
        event.stop_handling()

    class _ActionListObserver(klovve.data.list.List.Observer):

        def __init__(self, object_editor: "ObjectEditor",
                     viwid_object_editor: viwid.widgets.object_editor.ObjectEditor):
            super().__init__()
            self.__object_editor = object_editor
            self.__viwid_object_editor = viwid_object_editor

        def item_added(self, index, item):
            self.__viwid_object_editor.actions.insert(index, item)

        def item_removed(self, index, item):
            self.__viwid_object_editor.actions.pop(index)

    class _PropertyListObserver(klovve.data.list.List.Observer):

        def __init__(self, object_editor: "ObjectEditor",
                     viwid_object_editor: viwid.widgets.object_editor.ObjectEditor):
            super().__init__()
            self.__object_editor = object_editor
            self.__viwid_object_editor = viwid_object_editor

        def item_added(self, index, item):
            property_name, property_editor = item
            self.__viwid_object_editor.property_slots.insert(index, (
                property_name, self.__object_editor.materialize_child(property_editor).native))

        def item_removed(self, index, item):
            self.__viwid_object_editor.property_slots.pop(index)

    class _AdditionalViewsListObserver(klovve.data.list.List.Observer):

        def __init__(self, object_editor: "ObjectEditor",
                     viwid_object_editor: viwid.widgets.object_editor.ObjectEditor):
            super().__init__()
            self.__object_editor = object_editor
            self.__viwid_object_editor = viwid_object_editor

        def item_added(self, index, item):
            self.__viwid_object_editor.additional_widgets.insert(index,
                                                                 self.__object_editor.materialize_child(item).native)

        def item_removed(self, index, item):
            self.__viwid_object_editor.additional_widgets.pop(index)


class ObjectPropertyEditor(klovve.builtin.drivers.viwid.ViewMaterialization[klovve.views.ObjectPropertyEditor]):

    def create_native(self):
        viwid_object_property_editor = self.new_native(
            viwid.widgets.object_editor.ObjectPropertyEditor, self.piece,
            children_can_be_added_by_user=self.piece.bind.children_can_be_added_by_user)

        self.piece._introspect.observe_list_property(
            self.piece._introspect.property_by_name("children"),
            ObjectPropertyEditor._ChildrenListObserver, (self, viwid_object_property_editor), owner=self)
        viwid_object_property_editor.listen_event(
            viwid.widgets.object_editor.ObjectPropertyEditor.AddChildRequestedEvent, self.__handle_add_child_requested)

        return viwid_object_property_editor

    def __handle_add_child_requested(
            self, event: viwid.widgets.object_editor.ObjectPropertyEditor.AddChildRequestedEvent) -> None:
        self.piece.request_add_child()
        event.stop_handling()

    class _ChildrenListObserver(klovve.data.list.List.Observer):

        def __init__(self, object_property_editor: "ObjectPropertyEditor",
                     viwid_object_property_editor: viwid.widgets.object_editor.ObjectPropertyEditor):
            super().__init__()
            self.__object_property_editor = object_property_editor
            self.__viwid_object_property_editor = viwid_object_property_editor

        def item_added(self, index, item):
            item.horizontal_layout = klovve.ui.Layout(klovve.ui.Align.FILL_EXPANDING)
            self.__viwid_object_property_editor.object_editors.insert(
                index, self.__object_property_editor.materialize_child(item).native)

        def item_removed(self, index, item):
            self.__viwid_object_property_editor.object_editors.pop(index)


class ObjectEditorRoot(klovve.builtin.drivers.viwid.ViewMaterialization[klovve.views.ObjectEditorRoot]):

    def create_native(self):
        viwid_box = self.new_native(viwid.widgets.box.Box, self.piece, orientation=viwid.Orientation.VERTICAL)
        viwid_scrolled = self.new_native(
            viwid.widgets.scrollable.Scrollable)
        location_bar = klovve.views.ObjectEditorRoot._LocationBar()
        location_bar.location_selected_func = functools.partial(self.__handle_location_selected, viwid_scrolled,
                                                                location_bar)
        viwid_box.children.append(self.materialize_child(location_bar).native)
        viwid_box.children.append(viwid_scrolled)

        klovve.effect.activate_effect(klovve.builtin.drivers.viwid.ViewMaterialization.MaterializingViewEffect,
                                      (self, viwid_scrolled, lambda: self.piece.object_editor), owner=self)
        viwid_scrolled.listen_event(viwid.event.widget.ResizeEvent,
                                    lambda *_: self.__handle_scrolled(viwid_scrolled, location_bar))
        viwid_scrolled.listen_event(viwid.widgets.scrollable.Scrollable.OffsetChangedEvent,
                                    lambda *_: asyncio.get_running_loop().call_soon(
                                        lambda: self.__handle_scrolled(viwid_scrolled, location_bar)))

        self.__handle_scrolled(viwid_scrolled, location_bar)

        return viwid_box

    def __handle_location_selected(self, viwid_scrolled: viwid.widgets.scrollable.Scrollable,
                                   location_bar: "klovve.views.ObjectEditorRoot._LocationBar",
                                   object_editor: ObjectEditor) -> None:
        offset_y = viwid.app.screen.translate_coordinates_from_root(
            viwid.app.screen.translate_coordinates_to_root(
                viwid.Point(0, 0), old_origin=self.piece.object_editor._materialization.native)[0],
            new_origin=object_editor._materialization.native).y

        viwid_scrolled.scroll_to(viwid.Offset(0, -offset_y))
        asyncio.get_running_loop().call_later(0.5, lambda: self.__handle_scrolled(viwid_scrolled, location_bar))

    def __handle_scrolled(self, viwid_scrolled: viwid.widgets.scrollable.Scrollable,
                          location_bar: "klovve.views.ObjectEditorRoot._LocationBar") -> None:
        location_bar.is_visible = location_bar_is_visible = (
                self.piece.object_editor and
                (viwid_scrolled.vertical_scroll_max_offset > 0))
        if location_bar_is_visible:
            object_editors = []
            if self.piece.object_editor and self.piece.object_editor.is_expanded:
                object_editors.append((self.piece.object_editor,))

            segments = (self.piece.object_editor,)
            while object_editors:
                object_editor_segments = object_editors.pop()
                object_editor = object_editor_segments[-1]

                if viwid_object_editor := object_editor._materialization:
                    if viwid_object_editor2 := viwid_object_editor.native:

                        offset_y = viwid.app.screen.translate_coordinates_from_root(
                            viwid.app.screen.translate_coordinates_to_root(
                                viwid.Point(0, 0), old_origin=viwid_object_editor2)[0], new_origin=viwid_scrolled).y

                        if offset_y < 0 and viwid_object_editor2.size.height >= -offset_y:
                            segments = object_editor_segments

                for object_property_name, object_property_editor in object_editor.properties:
                    for child_object_editor in object_property_editor.children:
                        if child_object_editor.is_expanded:
                            object_editors.append(tuple((*object_editor_segments, child_object_editor)))

            location_bar.segments = segments
