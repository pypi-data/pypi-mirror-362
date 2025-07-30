#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve.drivers.gtk
import klovve.pieces.busy_animation

Gtk = klovve.drivers.gtk.Gtk


class View(klovve.pieces.busy_animation.View, klovve.drivers.gtk.View):

    @klovve.ComputedProperty
    def spinner_size(self):
        return {
            self.model.Size.TINY: (1, 1),
            self.model.Size.SMALL: (24, 24),
            self.model.Size.MEDIUM: (32, 32),
            self.model.Size.LARGE: (64, 64),
            self.model.Size.EXTRA_LARGE: (128, 128),
        }[self.model.size or self.model.Size.MEDIUM]

    @klovve.ComputedProperty
    def gtk_orientation(self):
        if self.model.orientation:
            v = self.model.orientation
        else:
            v = self.model.Orientation.HORIZONTAL if (self.model.size <= self.model.Size.TINY) else self.model.Orientation.VERTICAL
        return {
            self.model.Orientation.HORIZONTAL: Gtk.Orientation.HORIZONTAL,
            self.model.Orientation.VERTICAL: Gtk.Orientation.VERTICAL,
        }[v]

    def create_native(self):
        pieces, props = self.make_view()

        result = self.gtk_new(Gtk.Box, orientation=self.gtk_orientation)

        spinner = self.gtk_new(Gtk.Spinner, to_parent=result, spinning=True, hexpand=True, vexpand=True,
                               valign=Gtk.Align.CENTER)
        self.gtk_new(Gtk.Label, to_parent=result, hexpand=True, vexpand=True,
                     label=props(twoway=False, converter_in=lambda v: v or "").text,
                     visible=props(twoway=False, converter_in=lambda v: bool(v)).text)

        @klovve.reaction(owner=result)
        def __set_spinner_size():
            spinner.set_size_request(*self.spinner_size)  # TODO ?!?! see also dual?!

        return result
