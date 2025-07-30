#  SPDX-FileCopyrightText: © 2021 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve.pieces.progress
import klovve.drivers.gtk

Gtk = klovve.drivers.gtk.Gtk


class View(klovve.pieces.progress.View, klovve.drivers.gtk.View):

    def create_native(self):
        pieces, props = self.make_view()

        return self.gtk_new(Gtk.ProgressBar, fraction=props.value)
