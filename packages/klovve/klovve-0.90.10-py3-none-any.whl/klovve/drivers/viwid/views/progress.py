#  SPDX-FileCopyrightText: © 2021 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve.pieces.progress
import klovve.drivers.viwid


class View(klovve.pieces.progress.View, klovve.drivers.viwid.View):

    def create_native(self):
        pieces, props = self.make_view()

        return self.gtk_new(klovve.drivers.gtk.Gtk.ProgressBar, fraction=props.value)
