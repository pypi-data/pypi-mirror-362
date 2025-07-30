#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve.pieces.tabbed
import klovve.drivers.viwid

import viwid.widgets.box
import viwid.widgets.button
import viwid.widgets.widget
import viwid.canvas


class View(klovve.pieces.tabbed.View, klovve.drivers.viwid.View):

    def create_native(self):
        pieces, props = self.make_view()

        tab_bar = viwid.widgets.box.Box(
            orientation=viwid.widgets.box.Orientation.HORIZONTAL,
            horizontal_alignment=viwid.widgets.widget.Alignment.START
        )
        body = viwid.widgets.box.Box()
        pile = viwid.widgets.box.Box(
            orientation=viwid.widgets.box.Orientation.VERTICAL,
            children=[tab_bar, body],
            vertical_expand_greedily=True,
               horizontal_expand_greedily = True,
        )

        #@klovve.reaction(owner=self)
        def handle():
            for old_child in range(result.get_n_pages()):
                result.remove_page(-1)
            for item in model.items:
                itemview = item.view()
                with klovve.data.deps.no_dependency_tracking():  # TODO (otherwise studio tabs behave odd on first reload)
                    widget = itemview._model.item.view().native()

                #TODO even needed?!
                #if widget.props.parent:
                 #   widget.props.parent.remove(widget)

                result.append_page(widget)
                result.set_tab_label(widget, self.gtk_new(gtk.Label, label=props(model=itemview._model, twoway=False).label))

        def select_tab(widget):
            body.children = [widget] if widget else []

        def mkselect_tab(widget):
            def sh():
                select_tab(widget)
            return sh

        @klovve.reaction(owner=self)
        def handlecccc():
            if len(self.model.items) > 0 and not body.children:
                itemview = self.model.items[0].view()
                with klovve.data.deps.no_dependency_tracking():#TODO (otherwise studio tabs behave odd on first reload)
                    widget = itemview._model.item.view().native()
                select_tab(widget )

        @klovve.reaction(owner=self)
        def handle():
            #for old_child in range(result.get_n_pages()):
            #   result.remove_page(-1)
            for i, item in enumerate(self.model.items):
                itemview = item.view()

                with klovve.data.deps.no_dependency_tracking():#TODO (otherwise studio tabs behave odd on first reload)
                    widget = itemview._model.item.view().native()

                tab = viwid.widgets.button.Button()
                self.bind(tab, "text", props(model=itemview._model, twoway=False,
                                                  converter_in=lambda a: f"/ {a} \\").label)
                tab.on_click.append(mkselect_tab(widget))
                tab_bar.children.append(tab)
                tab_bar.children=tab_bar.children

        return pile
