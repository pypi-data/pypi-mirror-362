#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve.drivers.viwid
import klovve.pieces.split

import viwid.widgets.label
import viwid.widgets.box


class View(klovve.pieces.split.View, klovve.drivers.viwid.View):

    def create_native(self):
        pieces, props = self.make_view()

        empty_widget = viwid.widgets.label.Label
        cols = viwid.widgets.box.Box(
            orientation=viwid.widgets.box.Orientation.HORIZONTAL,
            #children=
        )
        cols.children = [empty_widget(), empty_widget()]


        @klovve.reaction(owner=cols)
        def set_item1():
            if self.model.item1:
                cols.children[0] = self.model.item1.view().native()
            else:
                cols.children[0] = empty_widget()
#                ss = self.urwid_as_box(model.item1)
 #               p1.original_widget = ss
#                paned.set_start_child(ss)
 #               fuh = ss.compute_expand(gtk.Orientation.HORIZONTAL)  # TODO
  #              paned.set_resize_start_child(fuh)
        #    else:
         #       paned.set_start_child(gtk.Label(visible=False)) #TODO paned.set_start_child(None)

        @klovve.reaction(owner=cols)
        def set_item2():
            if self.model.item2:
                cols.children[1] = self.model.item2.view().native()
            else:
                cols.children[1] = empty_widget()
                #ss = self.urwid_as_box(model.item2)
                #p2.original_widget = ss
                #paned.set_end_child(ss)
                #fuh = ss.compute_expand(gtk.Orientation.HORIZONTAL)
                #paned.set_resize_end_child(fuh)  # TODO
          #  else:
           #     paned.set_end_child(gtk.Label(visible=False)) #TODO paned.set_end_child(None)

        return cols
