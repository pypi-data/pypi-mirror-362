#  SPDX-FileCopyrightText: © 2021 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve.pieces.slider
import klovve.drivers.gtk

Gtk = klovve.drivers.gtk.Gtk


class View(klovve.pieces.slider.View, klovve.drivers.gtk.View):

    def create_native(self):
        pieces, props = self.make_view()

        scale = self.gtk_new(Gtk.Scale)

        self.bind(scale.props.adjustment, "step_increment", props(twoway=False).step_value)
        self.bind(scale.props.adjustment, "lower", props(twoway=False).min_value)
        self.bind(scale.props.adjustment, "upper", props(twoway=False).max_value)
        self.bind(scale.props.adjustment, "value", props.value)

        return scale
