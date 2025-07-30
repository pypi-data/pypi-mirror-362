#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve.drivers.gtk
import klovve.pieces.viewer.pdf

Gtk = klovve.drivers.gtk.Gtk


class View(klovve.pieces.viewer.pdf.View, klovve.BaseView):

    def create_native(self):
        pieces, props = self.make_view()

        mainscroll = Gtk.ScrolledWindow(visible=True, hexpand=True, vexpand=True)

        result = Gtk.Overlay()

        result.set_child(mainscroll)
        try:
            import gi
         #   gi.require_version("EvinceView", "4.0")
            from gi.repository import EvinceView
            from gi.repository import EvinceDocument
            EvinceDocument.init()
            btn_toc = Gtk.Button(image=Gtk.Image(stock="gtk-file"), halign=Gtk.Align.START, valign=Gtk.Align.START, margin_top=10, margin_start=30, visible=True)
            result.add_overlay(btn_toc)
            popover_toc = Gtk.Popover(relative_to=btn_toc)
            tocscroll = Gtk.ScrolledWindow(propagate_natural_width=True, propagate_natural_height=True, visible=True)
            popover_toc.add(tocscroll)
            lst_toc = Gtk.TreeView(headers_visible=False, activate_on_single_click=True, visible=True)
            tocscroll.add(lst_toc)
            lst_toc.append_column(Gtk.TreeViewColumn("", Gtk.CellRendererText(), text=0))
            def showtoc(_):
                popover_toc.popup()
            btn_toc.connect("clicked", showtoc)
            docview = EvinceView.View(visible=True)
            document = EvinceDocument.Document.factory_get_document(f"file://{self.model.path}")
            docview.set_model(EvinceView.DocumentModel.new_with_document(document))
            mainscroll.set_child(docview)
            def set_toc(job):
                lst_toc.props.model = job.get_model()
                topsection = lst_toc.props.model.get_iter_first()
                while topsection:
                    lst_toc.expand_row(lst_toc.props.model.get_path(topsection), False)
                    topsection = lst_toc.props.model.iter_next(topsection)
            joblinks = EvinceView.JobLinks.new(document)
            joblinks.connect("finished", set_toc)
            joblinks.run()
            def goto(_, row, __):
                foo = lst_toc.props.model.get(lst_toc.props.model.get_iter(row), 1)[0]
                docview.handle_link(foo)
            lst_toc.connect("row-activated", goto)

        except ImportError:
            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, visible=True)
            mainscroll.set_child(box)
            box.append(Gtk.Label(label="Please find the Krrez documentation here:", wrap=True))
            btnopen = Gtk.LinkButton(label=str(self.model.path), visible=True)
            btnopen.props.uri = f"file://{self.model.path}"  # TODO can we open files in devlab this way?!
            box.append(btnopen)

        return result
