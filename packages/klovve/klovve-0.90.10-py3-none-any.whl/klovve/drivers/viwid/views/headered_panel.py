#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import asyncio

import klovve.app
import klovve.drivers.viwid
import klovve.pieces.headered_panel
import viwid.widgets.label
import viwid.widgets.box
import viwid.widgets.busy_animation
import viwid.widgets.progress_bar
import viwid.widgets.widget


class Model(klovve.pieces.headered_panel.Model):

    @klovve.ComputedProperty
    def title_label_background(self):
        if self.state == self.State.BUSY:
            return None
        elif self.state == self.State.SUCCESSFUL:
            return "#0f0"
        elif self.state == self.State.SUCCESSFUL_WITH_WARNING:
            return "#fb0"
        elif self.state == self.State.FAILED:
            return "#f00"
        else:
            return None


class View(klovve.pieces.headered_panel.View, klovve.drivers.viwid.View):

    def create_native(self):
        pieces, props = self.make_view()

        indicbox = viwid.widgets.box.Box()
        hdlabel = viwid.widgets.label.Label()
        tsi = viwid.widgets.box.Box(
            orientation=viwid.widgets.box.Orientation.HORIZONTAL,
            horizontal_expand_greedily=False,
        )
        hdibox = viwid.widgets.box.Box(
            children=[viwid.widgets.label.Label(text="  ", horizontal_expand_greedily=True), indicbox,
                      viwid.widgets.label.Label(text="  "), hdlabel,
                      viwid.widgets.label.Label(text="  ", horizontal_expand_greedily=True), tsi],
            orientation=viwid.widgets.box.Orientation.HORIZONTAL,
        )
        hdbox = viwid.widgets.box.Box(
            orientation=viwid.widgets.box.Orientation.HORIZONTAL,
            children=[hdibox],
            horizontal_expand_greedily=True,
        )
        progressbar = viwid.widgets.progress_bar.ProgressBar(
            #vertical_expand_greedily=True,
        )
        body_box = viwid.widgets.box.Box()

        box = viwid.widgets.box.Box(
            children=[hdbox,progressbar,body_box],
            orientation=viwid.widgets.box.Orientation.VERTICAL
        )

        @klovve.reaction(owner=box)
        def fddfdf():
            if self.model.state == self.model.State.BUSY:
                a = [viwid.widgets.busy_animation.BusyAnimation()]
            elif self.model.state == self.model.State.SUCCESSFUL:
                a = [viwid.widgets.label.Label(text="✓")]
            elif self.model.state == self.model.State.SUCCESSFUL_WITH_WARNING:
                a = [viwid.widgets.label.Label(text="TODO")]
            elif self.model.state == self.model.State.FAILED:
                a = [viwid.widgets.label.Label(text="×")]
            else:
                a = []
            indicbox.children = a

        @klovve.reaction(owner=box)
        def ddsfd():
            tsi.children = [x.view().native() for x in self.model.title_secondary_items]

        @klovve.reaction(owner=box)
        def ddd():
            hdlabel.text = self.model.title

        @klovve.reaction(owner=box)
        def dddf():
            progressbar.value = self.model.progress

        @klovve.reaction(owner=box)
        def fdddf():
            hdbox.background = self.model.title_label_background

    #        gtk = klovve.drivers.gtk.Gtk
 #       box = self.gtk_new(gtk.Box, orientation=gtk.Orientation.VERTICAL)
  #      header_bar = self.gtk_new(gtk.HeaderBar, show_title_buttons=False)
   #     box.append(header_bar)
    #    progressbar = self.gtk_new(gtk.ProgressBar, fraction=model_bind(twoway=False).progress)
     #   box.append(progressbar)
      #  ibox = self.gtk_new(gtk.Box)
       # box.append(ibox)
#        title_box = self.gtk_new(gtk.Box, orientation=gtk.Orientation.HORIZONTAL)
 #       state_box = self.gtk_new(gtk.Box, orientation=gtk.Orientation.HORIZONTAL, css_classes=["headered_state_box"])
  #      title_label = self.gtk_new(gtk.Label, label=model_bind(twoway=False).title,
   #                                css_classes=model_bind.title_label_css_classes)
   #     title_box.append(state_box)
    #    title_box.append(title_label)
     #   header_bar.set_title_widget(title_box)
      #  header_bar.pack_end(self._view_factory.horizontal_box(items=model_bind.title_secondary_items).view().native())

#        @klovve.reaction(owner=box)
 #       def _handle_state():
  #          for old_widget in klovve.drivers.gtk.children(state_box):
   #             state_box.remove(old_widget)
    #        if model.state == klovve.pieces.headered_panel.Model.State.BUSY:
     #           state_box.append(self.gtk_new(gtk.Spinner, spinning=True))
      #      elif model.state == klovve.pieces.headered_panel.Model.State.SUCCESSFUL:
       #         state_box.append(gtk.Image.new_from_icon_name("dialog-ok"))
        #    elif model.state == klovve.pieces.headered_panel.Model.State.SUCCESSFUL_WITH_WARNING:
         #       state_box.append(gtk.Image.new_from_icon_name("dialog-warning"))
          #  elif model.state == klovve.pieces.headered_panel.Model.State.FAILED:
           #     state_box.append(gtk.Image.new_from_icon_name("dialog-error"))
#            else:
 #               title_label.set_css_classes([])

        @klovve.reaction(owner=box)
        def set_item():
            body_box.children = [self.model.body.view().native()] if self.model.body else []

        return box
