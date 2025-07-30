# SPDX-FileCopyrightText: © 2025 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only
import asyncio
import functools

import klovve.builtin.drivers.gtk
from klovve.builtin.drivers.gtk import GObject, Gtk, Graphene
import klovve.data


class ObjectEditor(klovve.builtin.drivers.gtk.ViewMaterialization[klovve.views.ObjectEditor]):

    def create_native(self):
        gtk_object_editor = self.new_native(
            _GtkObjectEditor, self.piece, title=self.piece.bind.title, coloration=self.piece.bind.coloration,
            is_removable_by_user=self.piece.bind.is_removable_by_user, is_expanded=self.piece.bind.is_expanded)

        self.piece._introspect.observe_list_property(
            self.piece._introspect.property_by_name("actions"),
            ObjectEditor._ActionListObserver, (self, gtk_object_editor), owner=self)
        self.piece._introspect.observe_list_property(
            self.piece._introspect.property_by_name("properties"),
            ObjectEditor._PropertyListObserver, (self, gtk_object_editor), owner=self)
        self.piece._introspect.observe_list_property(
            self.piece._introspect.property_by_name("additional_views"),
            ObjectEditor._AdditionalViewsListObserver, (self, gtk_object_editor), owner=self)
        gtk_object_editor.connect("execute_action_requested",
                                  lambda _, action_name: self.piece.trigger_action(action_name))
        gtk_object_editor.connect("remove_requested", lambda *_: self.piece.request_remove())

        return gtk_object_editor

    class _ActionListObserver(klovve.data.list.List.Observer):

        def __init__(self, object_editor: "ObjectEditor", gtk_object_editor: "_GtkObjectEditor"):
            super().__init__()
            self.__object_editor = object_editor
            self.__gtk_object_editor = gtk_object_editor

        def item_added(self, index, item):
            action_label, action_name = item
            self.__gtk_object_editor.add_action(index, label=action_label, action_name=action_name)

        def item_removed(self, index, item):
            self.__gtk_object_editor.remove_action(index)

    class _PropertyListObserver(klovve.data.list.List.Observer):

        def __init__(self, object_editor: "ObjectEditor", gtk_object_editor: "_GtkObjectEditor"):
            super().__init__()
            self.__object_editor = object_editor
            self.__gtk_object_editor = gtk_object_editor

        def item_added(self, index, item):
            property_name, property_editor = item
            self.__gtk_object_editor.add_property_slot(
                index, property_name=property_name,
                property_editor=self.__object_editor.materialize_child(property_editor).native)

        def item_removed(self, index, item):
            self.__gtk_object_editor.remove_property_slot(index)

    class _AdditionalViewsListObserver(klovve.data.list.List.Observer):

        def __init__(self, object_editor: "ObjectEditor", gtk_object_editor: "_GtkObjectEditor"):
            super().__init__()
            self.__object_editor = object_editor
            self.__gtk_object_editor = gtk_object_editor

        def item_added(self, index, item):
            self.__gtk_object_editor.add_additional_widget(index,
                                                           widget=self.__object_editor.materialize_child(item).native)

        def item_removed(self, index, item):
            self.__gtk_object_editor.remove_additional_widget(index)


class ObjectPropertyEditor(klovve.builtin.drivers.gtk.ViewMaterialization[klovve.views.ObjectPropertyEditor]):

    def create_native(self):
        gtk_object_property_editor = self.new_native(
            _GtkObjectPropertyEditor, self.piece,
            children_can_be_added_by_user=self.piece.bind.children_can_be_added_by_user)

        self.piece._introspect.observe_list_property(
            self.piece._introspect.property_by_name("children"),
            ObjectPropertyEditor._ChildrenListObserver, (self, gtk_object_property_editor), owner=self)
        gtk_object_property_editor.connect("add_child_requested", lambda *_: self.piece.request_add_child())

        return gtk_object_property_editor

    class _ChildrenListObserver(klovve.data.list.List.Observer):

        def __init__(self, object_property_editor: "ObjectPropertyEditor",
                     gtk_object_property_editor: "_GtkObjectPropertyEditor"):
            super().__init__()
            self.__object_property_editor = object_property_editor
            self.__gtk_object_property_editor = gtk_object_property_editor

        def item_added(self, index, item):
            item.horizontal_layout = klovve.ui.Layout(klovve.ui.Align.FILL_EXPANDING)
            self.__gtk_object_property_editor.add_object_editor(
                index, object_editor=self.__object_property_editor.materialize_child(item).native)

        def item_removed(self, index, item):
            self.__gtk_object_property_editor.remove_object_editor(index)


class ObjectEditorRoot(klovve.builtin.drivers.gtk.ViewMaterialization[klovve.views.ObjectEditorRoot]):

    def create_native(self):
        gtk_box = self.new_native(Gtk.Box, self.piece, orientation=Gtk.Orientation.VERTICAL)
        gtk_scrolled = self.new_native(
            Gtk.ScrolledWindow, halign=Gtk.Align.FILL, valign=Gtk.Align.FILL, hexpand=True, vexpand=True,
            overlay_scrolling=False)
        location_bar = klovve.views.ObjectEditorRoot._LocationBar()
        location_bar.location_selected_func = functools.partial(self.__handle_location_selected, gtk_scrolled,
                                                                location_bar)
        gtk_box.append(self.materialize_child(location_bar).native)
        gtk_box.append(gtk_scrolled)

        klovve.effect.activate_effect(klovve.builtin.drivers.gtk.ViewMaterialization.MaterializingViewEffect,
                                      (self, gtk_scrolled, lambda: self.piece.object_editor), owner=self)
        gtk_scrolled.get_vadjustment().connect("changed", lambda *_: self.__handle_scrolled(gtk_scrolled, location_bar))
        gtk_scrolled.get_vadjustment().connect("value-changed",
                                               lambda *_: asyncio.get_running_loop().call_soon(
                                                   lambda: self.__handle_scrolled(gtk_scrolled, location_bar)))
        self.__handle_scrolled(gtk_scrolled, location_bar)

        return gtk_box

    def __handle_location_selected(self, gtk_scrolled: Gtk.ScrolledWindow,
                                   location_bar: klovve.views.ObjectEditorRoot._LocationBar,
                                   object_editor: ObjectEditor) -> None:
        y_offset = object_editor._materialization.native.compute_point(
            self.piece.object_editor._materialization.native, Graphene.Point(0, 0))[1].y
        gtk_scrolled.get_vadjustment().set_value(y_offset)
        asyncio.get_running_loop().call_later(0.5, lambda: self.__handle_scrolled(gtk_scrolled, location_bar))

    def __handle_scrolled(self, gtk_scrolled: Gtk.ScrolledWindow,
                          location_bar: klovve.views.ObjectEditorRoot._LocationBar) -> None:
        gtk_scrolled_vadjustment = gtk_scrolled.get_vadjustment()
        location_bar.is_visible = location_bar_is_visible = (
                self.piece.object_editor and
                (gtk_scrolled_vadjustment.get_page_size() != gtk_scrolled_vadjustment.get_upper()))
        if location_bar_is_visible:
            object_editors = []
            if self.piece.object_editor and self.piece.object_editor.is_expanded:
                object_editors.append((self.piece.object_editor,))

            segments = (self.piece.object_editor,)
            while object_editors:
                object_editor_segments = object_editors.pop()
                object_editor = object_editor_segments[-1]

                if gtk_object_editor := object_editor._materialization:
                    if gtk_object_editor2 := gtk_object_editor.native:
                        offset_y = gtk_object_editor2.compute_point(gtk_scrolled, Graphene.Point(0, 0))[1].y

                        if offset_y < -10 and gtk_object_editor2.get_size(Gtk.Orientation.VERTICAL) >= -offset_y:
                            segments = object_editor_segments

                for object_property_name, object_property_editor in object_editor.properties:
                    for child_object_editor in object_property_editor.children:
                        if child_object_editor.is_expanded:
                            object_editors.append(tuple((*object_editor_segments, child_object_editor)))

            location_bar.segments = segments


class _GtkObjectEditor(Gtk.Stack):

    def __init__(self, **kwargs):
        self.__description_label = ""
        self.__icon_name = ""
        self.__is_removable_by_user = False
        self.__expanded = False
        self.__coloration = klovve.views.ObjectEditor.Coloration.GRAY
        self.__remove_button = Gtk.Button(valign=Gtk.Align.START, halign=Gtk.Align.END, icon_name="edit-delete",
                                          hexpand=True, css_classes=("flat",))
        self.__node_header_collapsed = _GtkObjectEditor._GtkNodeHeader()
        self.__node_header_expanded = _GtkObjectEditor._GtkNodeHeader()
        self.__header_button_collapsed = Gtk.Button(child=self.__node_header_collapsed, halign=Gtk.Align.FILL,
                                                    hexpand=True, css_classes=("klv_object_editor__collapsed",))
        self.__header_button_expanded = Gtk.Button(child=self.__node_header_expanded, valign=Gtk.Align.START,
                                                   hexpand=True, css_classes=("klv_object_editor_title_button",))
        self.__actions_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,
                                     css_classes=("klv_object_editor_action_box",))
        inner_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, halign=Gtk.Align.FILL, hexpand=True,
                            css_classes=("klv_object_editor__expanded",))
        inner_box.append(inner_head_box := Gtk.Box(orientation=Gtk.Orientation.VERTICAL))
        self.__property_grid = Gtk.Grid(row_spacing=4, css_classes=("klv_object_editor_property_grid",))
        inner_box.append(self.__property_grid)
        self.__additional_widgets_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        super().__init__(**kwargs, interpolate_size=True, transition_type=Gtk.StackTransitionType.CROSSFADE,
                         halign=Gtk.Align.START, vhomogeneous=False, hhomogeneous=False, css_name="klv_object_editor")

        self.__header_button_collapsed.connect("clicked", self.__clicked)
        self.__header_button_expanded.connect("clicked", self.__clicked)
        self.__remove_button.connect("clicked", lambda *_: self.emit("remove_requested"))
        self.add_named(inner_box, "box")
        self.add_named(self.__header_button_collapsed, "button")
        inner_head_box.append(header_button_expanded_overlay := Gtk.Overlay(child=self.__header_button_expanded))
        header_button_expanded_overlay.add_overlay(self.__remove_button)
        inner_head_box.append(self.__actions_box)
        inner_head_box.append(self.__additional_widgets_box)

        self.title = self.title
        self.coloration = self.coloration
        self.is_removable_by_user = self.is_removable_by_user
        self.is_expanded = self.is_expanded

    @GObject.property
    def title(self) -> str:
        return self.__description_label

    @title.setter
    def title(self, _: str) -> None:
        self.__description_label = _
        for node_header in (self.__node_header_collapsed, self.__node_header_expanded):
            node_header.text = _

    def set_title(self, _: str) -> None:
        self.title = _

    @GObject.property
    def coloration(self) -> klovve.views.ObjectEditor.Coloration:
        return self.__coloration

    @coloration.setter
    def coloration(self, _: klovve.views.ObjectEditor.Coloration) -> None:
        self.__coloration = _
        self.set_css_classes((f"klv_object_editor__coloration_{_.name}",))

    def set_coloration(self, _: klovve.views.ObjectEditor.Coloration) -> None:
        self.coloration = _

    @GObject.property
    def is_removable_by_user(self) -> bool:
        return self.__is_removable_by_user

    @is_removable_by_user.setter
    def is_removable_by_user(self, _: bool) -> None:
        self.__is_removable_by_user = _
        self.__remove_button.set_visible(_)

    def set_is_removable_by_user(self, _: bool) -> None:
        self.is_removable_by_user = _

    @GObject.property
    def is_expanded(self) -> bool:
        return self.__expanded

    @is_expanded.setter
    def is_expanded(self, _: bool) -> None:
        self.__expanded = bool(_)
        was_focused = self.__header_button_expanded.has_focus() or self.__header_button_collapsed.has_focus()
        self.set_visible_child_name("box" if _ else "button")
        if was_focused:
            (self.__header_button_expanded if _ else self.__header_button_collapsed).grab_focus()

    def set_is_expanded(self, _: bool) -> None:
        self.is_expanded = _

    def add_action(self, i: int, *, label: str, action_name: str) -> None:
        action_button = Gtk.Button(label=label, halign=Gtk.Align.END, css_classes=("flat", "klv_button_link"))
        action_button.connect("clicked", lambda *_: self.emit("execute_action_requested", action_name))
        klovve.builtin.drivers.gtk.ViewMaterialization.add_child_view_native(self.__actions_box, i, action_button)

    def remove_action(self, i: int) -> None:
        klovve.builtin.drivers.gtk.ViewMaterialization.remove_child_view_native(self.__actions_box, i)

    def add_property_slot(self, i: int, *, property_name: str, property_editor: "_GtkObjectPropertyEditor") -> None:
        property_name = property_name or ""
        self.__property_grid.insert_row(i)
        self.__property_grid.attach(Gtk.Label(label=f"{property_name}:" if property_name else "", xalign=1, yalign=0,
                                              css_classes=("klv_object_editor_property_label",)), 0, i, 1, 1)
        self.__property_grid.attach(property_editor, 1, i, 1, 1)

    def remove_property_slot(self, i: int) -> None:
        self.__property_grid.remove_row(i)

    def add_additional_widget(self, i: int, *, widget: Gtk.Widget) -> None:
        klovve.builtin.drivers.gtk.ViewMaterialization.add_child_view_native(self.__additional_widgets_box, i, widget)

    def remove_additional_widget(self, i: int) -> None:
        klovve.builtin.drivers.gtk.ViewMaterialization.remove_child_view_native(self.__additional_widgets_box, i)

    @GObject.Signal(arg_types=[str])
    def execute_action_requested(self, *_):
        pass

    @GObject.Signal()
    def remove_requested(self):
        pass

    def __clicked(self, *_) -> None:
        self.is_expanded = not self.is_expanded

    class _GtkNodeHeader(Gtk.Box):

        def __init__(self, **kwargs):
            self.__label = Gtk.Label()
            super().__init__(**kwargs, hexpand=True)
            self.append(self.__label)

        @GObject.property
        def text(self) -> str:
            return self.__label.get_label()

        @text.setter
        def text(self, value) -> None:
            self.__label.set_label(value)


class _GtkObjectPropertyEditor(Gtk.Box):

    def __init__(self, **kwargs):
        self.__add_child_button = Gtk.Button(halign=Gtk.Align.FILL, icon_name="list-add",
                                             css_classes=("klv_object_property_editor_add_child_button",))

        super().__init__(**kwargs, orientation=Gtk.Orientation.VERTICAL, css_name="klv_object_property_editor")

        self.__child_object_editors_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.append(self.__child_object_editors_box)
        self.append(self.__add_child_button)
        self.__add_child_button.connect("clicked", lambda _: self.emit("add_child_requested"))

        self.children_can_be_added_by_user = self.children_can_be_added_by_user

    @GObject.property
    def children_can_be_added_by_user(self) -> bool:
        return self.__add_child_button.get_visible()

    @children_can_be_added_by_user.setter
    def children_can_be_added_by_user(self, _: bool) -> None:
        self.__add_child_button.set_visible(_)

    def set_children_can_be_added_by_user(self, _: bool) -> None:
        self.children_can_be_added_by_user = _

    def add_object_editor(self, i: int, *, object_editor: "_GtkObjectEditor") -> None:
        object_editor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, halign=object_editor.props.halign)
        klovve.builtin.drivers.gtk.ViewMaterialization.add_child_view_native(self.__child_object_editors_box, i,
                                                                             object_editor_box)
        object_editor_box.append(object_editor)

    def remove_object_editor(self, i: int) -> None:
        klovve.builtin.drivers.gtk.ViewMaterialization.remove_child_view_native(self.__child_object_editors_box, i)

    @GObject.Signal()
    def add_child_requested(self, *args):
        pass
