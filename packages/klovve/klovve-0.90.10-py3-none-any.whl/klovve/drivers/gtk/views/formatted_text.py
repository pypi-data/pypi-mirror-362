#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve.drivers.gtk
import klovve.pieces.formatted_text
import xml.etree.ElementTree

Gtk = klovve.drivers.gtk.Gtk


class View(klovve.pieces.formatted_text.View, klovve.drivers.gtk.View):

    def create_native(self):  # TODO scrolling?!
        pieces, props = self.make_view()

        text_view = self.gtk_new(Gtk.TextView, hexpand=True, vexpand=True, editable=False,
                                 cursor_visible=False, wrap_mode=Gtk.WrapMode.WORD)

        buf = text_view.props.buffer

#TODO
        buf.create_tag("body")
        buf.create_tag("h1", pixels_above_lines=10, left_margin=20, size=klovve.drivers.gtk.Pango.SCALE * 25)
        buf.create_tag("ul")
        buf.create_tag("li")
        buf.create_tag("foo", size=klovve.drivers.gtk.Pango.SCALE * 15)

        def put(x):
            start_mark = buf.create_mark("", buf.get_end_iter(), True)

            if x.tag.lower() in ["ul", "li"]:
                buf.insert(buf.get_end_iter(), "\n")

            buf.insert(buf.get_end_iter(), x.text or "")#TODO, x.tag.lower())
            for xc in x:
                put(xc)
            if x.tag.lower() in ["h1", "ul", "li"]:
                buf.insert(buf.get_end_iter(), "\n")

            buf.apply_tag_by_name(x.tag.lower(), buf.get_iter_at_mark(start_mark), buf.get_end_iter())
            buf.insert(buf.get_end_iter(), x.tail or "")

        @klovve.reaction(owner=text_view)
        def __set_text():
            xmldoc = xml.etree.ElementTree.fromstring("<body>"+self.model.text+"</body>")
            buf.set_text("")
            put(xmldoc)

        return text_view


"""
        self.__tag_title = self.__text.create_tag("title", pixels_above_lines=10,
                                                  left_margin=20, size=Pango.SCALE * 25)
        self.__tag_main = self.__text.create_tag("main", pixels_above_lines=10, size=Pango.SCALE * 11)
        self.__tag_item_title = self.__text.create_tag("item_title", pixels_above_lines=10, size=Pango.SCALE * 14)
        self.__tag_item = self.__text.create_tag("item", size=Pango.SCALE * 11)
        super().__init__(**kwargs)
        self.add(textview)
        self.viewkinds = []

    @GObject.Property
    def viewkinds(self):
        return self.__viewkinds

    @viewkinds.setter
    def viewkinds(self, value):
        self.__viewkinds = value
        self.__text.delete(self.__text.get_start_iter(), self.__text.get_end_iter())
        self.__text.insert_with_tags(self.__text.get_end_iter(), self._TITLE + "\n", self.__tag_title)
        self.__text.insert_with_tags(self.__text.get_end_iter(), self._MAIN + "\n", self.__tag_main)
        for kindname in value or ():
            tab_title, tab_description = self._TABS[kindname]
            self.__text.insert_with_tags(self.__text.get_end_iter(), tab_title + ": ", self.__tag_item_title)
            self.__text.insert_with_tags(self.__text.get_end_iter(), tab_description + "\n", self.__tag_item)
"""