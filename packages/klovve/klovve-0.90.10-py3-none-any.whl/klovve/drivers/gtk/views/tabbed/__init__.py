#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve
import klovve.pieces.tabbed
import klovve.drivers.gtk

Gtk = klovve.drivers.gtk.Gtk


class View(klovve.pieces.tabbed.View, klovve.drivers.gtk.View):

    def create_native(self):
        pieces, props = self.make_view()

        #kind = self.get_hint("kind", "foo")#TODO
        result = self.gtk_new(Gtk.Notebook)

        @klovve.reaction(owner=self)
        def handle():
            for old_child in range(result.get_n_pages()):
                result.remove_page(-1)
            for item in self.model.items:
                itemview = item.view()
                with klovve.data.deps.no_dependency_tracking():#TODO (otherwise studio tabs behave odd on first reload)
                    widget = itemview._model.item.view().native()

                #TODO even needed?!
                #if widget.props.parent:
                 #   widget.props.parent.remove(widget)

                result.append_page(widget)
                result.set_tab_label(widget, self.gtk_new(Gtk.Label, label=props(model=itemview._model, twoway=False).label))

        return result
