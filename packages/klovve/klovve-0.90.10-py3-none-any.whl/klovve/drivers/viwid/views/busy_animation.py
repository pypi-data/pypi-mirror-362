#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve.drivers.viwid
import klovve.pieces.busy_animation

import viwid.widgets.label


class Model(klovve.pieces.busy_animation.Model):

    #@klovve.ComputedProperty
    def spinner_size(self):
        return {
            self.Size.TINY: (1, 1),
            self.Size.SMALL: (24, 24),
            self.Size.MEDIUM: (32, 32),
            self.Size.LARGE: (64, 64),
            self.Size.EXTRA_LARGE: (128, 128),
        }[self.size or self.Size.MEDIUM]

    #@klovve.ComputedProperty
    def gtk_orientation(self):
        gtk = klovve.drivers.gtk.Gtk
        if self.orientation:
            v = self.orientation
        else:
            v = self.Orientation.HORIZONTAL if (self.size <= self.Size.TINY) else self.Orientation.VERTICAL
        return {
            self.Orientation.HORIZONTAL: gtk.Orientation.HORIZONTAL,
            self.Orientation.VERTICAL: gtk.Orientation.VERTICAL,
        }[v]


class View(klovve.pieces.busy_animation.View, klovve.drivers.viwid.View):

    model: Model

    def create_native(self):
        pieces, props = self.make_view()

        return viwid.widgets.label.Label(text="TODO busy")
