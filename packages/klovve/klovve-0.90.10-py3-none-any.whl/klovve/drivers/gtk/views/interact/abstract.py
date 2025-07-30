#  SPDX-FileCopyrightText: © 2021 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve.pieces.interact.abstract
import klovve.drivers.gtk

Gtk = klovve.drivers.gtk.Gtk


class View(klovve.pieces.interact.abstract.View, klovve.drivers.gtk.View):

    def create_native(self):
        pieces, props = self.make_view()

        box = self.gtk_new(Gtk.Box, orientation=Gtk.Orientation.VERTICAL, hexpand=True,
                           css_classes=["klovve_interact_box"])
        box.append(self.gtk_new(Gtk.Label, wrap=True, label=props(twoway=False).message))
        inner_box = self.gtk_new(Gtk.Box, orientation=Gtk.Orientation.VERTICAL)
        box.append(inner_box)
        trigger_box = self.gtk_new(Gtk.Box, orientation=Gtk.Orientation.VERTICAL)
        box.append(trigger_box)

        @klovve.reaction(owner=self)
        def on_inner_changed():
            for old_item in klovve.drivers.gtk.children(inner_box):
                inner_box.remove(old_item)
            if self.model.inner_view:
                inner_box.append(self.model.inner_view.view().native())

        @klovve.reaction(owner=self)
        def on_triggers_changed():
            for old_item in klovve.drivers.gtk.children(trigger_box):
                trigger_box.remove(old_item)
            def mkfoo(i):
                def foo(_):
                    self.model.set_answer(self.model.get_answer_func(i))
                return foo
            for i, trigger_text in enumerate(self.model.triggers):
                btn = self.gtk_new(Gtk.Button, label=trigger_text)
                trigger_box.append(btn)
                btn.connect("clicked", mkfoo(i))

        return box
