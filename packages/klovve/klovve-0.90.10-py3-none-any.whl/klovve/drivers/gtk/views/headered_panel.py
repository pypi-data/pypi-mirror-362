#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import asyncio
import klovve.app
import klovve.drivers.gtk
import klovve.pieces.headered_panel

Gtk = klovve.drivers.gtk.Gtk


class View(klovve.pieces.headered_panel.View, klovve.drivers.gtk.View):

    @klovve.ComputedProperty
    def title_label_css_classes(self):
        state, State = self.model.state, self.model.State
        if state == State.BUSY:
            return ["headered_title_busy"]
        elif state == State.SUCCESSFUL:
            return ["headered_title_successful"]
        elif state == State.SUCCESSFUL_WITH_WARNING:
            return ["headered_title_successful_with_warning"]
        elif state == State.FAILED:
            return ["headered_title_failed"]
        else:
            return []

    def create_native(self):
        pieces, props = self.make_view()

        result = self.gtk_new(Gtk.Box, orientation=Gtk.Orientation.VERTICAL)

        header_bar = self.gtk_new(Gtk.HeaderBar, to_parent=result, show_title_buttons=False)
        header_bar.pack_end(self._view_factory.horizontal_box(items=props.title_secondary_items).view().native())
        header_bar.pack_start(self._view_factory.horizontal_box(items=props.actions).view().native())

        self.gtk_new(Gtk.ProgressBar, to_parent=result, fraction=props(twoway=False).progress)

        body_box = self.gtk_new(Gtk.Box, to_parent=result)

        title_box = self.gtk_new(Gtk.Box, orientation=Gtk.Orientation.HORIZONTAL)
        header_bar.set_title_widget(title_box)

        state_box = self.gtk_new(Gtk.Box, to_parent=title_box, orientation=Gtk.Orientation.HORIZONTAL,
                                 css_classes=["headered_state_box"])

        title_label = self.gtk_new(Gtk.Label, to_parent=title_box, label=props(twoway=False).title,
                                   css_classes=props.title_label_css_classes)

        @klovve.reaction(owner=result)
        def __handle_state():
            state, State = self.model.state, self.model.State
            for old_widget in klovve.drivers.gtk.children(state_box):
                state_box.remove(old_widget)
            if state == State.BUSY:
                state_box.append(self.gtk_new(Gtk.Spinner, spinning=True))
            elif state == State.SUCCESSFUL:
                state_box.append(Gtk.Image.new_from_icon_name("dialog-ok"))
            elif state == State.SUCCESSFUL_WITH_WARNING:
                state_box.append(Gtk.Image.new_from_icon_name("dialog-warning"))
            elif state == State.FAILED:
                state_box.append(Gtk.Image.new_from_icon_name("dialog-error"))
            else:
                title_label.set_css_classes([])

        @klovve.reaction(owner=result)
        def __set_body():
            for old_child in self.gtk_children(body_box):
                body_box.remove(old_child)
            if self.model.body:
                body_box.append(self.model.body.view().native())

        return result
