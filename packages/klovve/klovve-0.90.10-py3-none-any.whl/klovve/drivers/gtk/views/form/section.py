#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve.drivers.gtk
import klovve.pieces.form.section

Gtk = klovve.drivers.gtk.Gtk


class View(klovve.pieces.form.section.View, klovve.drivers.gtk.View):

    def create_native(self):
        pieces, props = self.make_view()

        result = self.gtk_new(Gtk.Box, orientation=Gtk.Orientation.VERTICAL)

        result.get_style_context().add_class("klovve_form_section")

        label = self.gtk_new(Gtk.Label, label=props(twoway=False).label)
        result.append(label)

        content = self.gtk_new(Gtk.Box)
        result.append(content)

        @klovve.reaction(owner=self)
        def __on_compute_label_visibility():
            label.set_visible(self.model.item and self.model.label)

        @klovve.reaction(owner=self)
        def __on_item_changed():
            for old_child in klovve.drivers.gtk.children(content):
                content.remove(old_child)
            if self.model.item:
                content.append(self.model.item.view().native())

        return result
