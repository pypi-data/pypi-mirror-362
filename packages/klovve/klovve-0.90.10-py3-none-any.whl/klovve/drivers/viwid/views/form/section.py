#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve.drivers.viwid
import klovve.pieces.form.section

import viwid.widgets.label
import viwid.widgets.box


class View(klovve.pieces.form.section.View, klovve.drivers.viwid.View):

    def create_native(self):
        pieces, props = self.make_view()

        result = viwid.widgets.label.Label()
        placeholder = viwid.widgets.box.Box()
        pile = viwid.widgets.box.Box(children=[result, placeholder], orientation=viwid.widgets.box.Orientation.VERTICAL)

        @klovve.reaction(owner=result)
        def TODO():
            result.text = self.model.label

        @klovve.reaction(owner=result)
        def TODOx():
            placeholder.children = [self.model.item.view().native()] if self.model.item else []

        return pile





        gtk = klovve.drivers.gtk.Gtk
        result = self.gtk_new(gtk.Box, orientation=gtk.Orientation.VERTICAL)

        result.get_style_context().add_class("klovve_form_section")

        label = self.gtk_new(gtk.Label, label=props(twoway=False).label)
        result.append(label)

        content = self.gtk_new(gtk.Box)
        result.append(content)

        @klovve.reaction(owner=self)
        def on_compute_label_visibility():
            label.set_visible(model.item and model.label)

        @klovve.reaction(owner=self)
        def on_item_changed():
            for old_child in klovve.drivers.gtk.children(content):
                content.remove(old_child)
            if model.item:
                content.append(model.item.view().native())

        return result
