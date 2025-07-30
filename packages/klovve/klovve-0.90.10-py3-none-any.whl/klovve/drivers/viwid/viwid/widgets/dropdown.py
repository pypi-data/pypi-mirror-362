#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import functools
import viwid.widgets.button
import viwid.widgets.box
import viwid.widgets.frame
import viwid.widgets.label
import viwid.widgets.widget
import viwid.screen


class DropDown(viwid.widgets.button.Button):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.on_click.append(self.__click)
        self.selected_index = None

    @viwid.widgets.widget.ListProperty(lambda *_: None, lambda *_: None)
    def items(self):
        pass

    @viwid.widgets.widget.Property
    def selected_index(self, v):
        self.selected_item = self.items[v] if (v is not None) else None

    @viwid.widgets.widget.Property
    def selected_item(self, v):
        try:
         idx = self.items.index(v) if (v is not None) else None
        except ValueError:
            idx = None
        if idx != self.selected_index:
            self.selected_index = idx
            return
        self.text = v if (v is not None) else "----"

    def _select(self, i):
        self.selected_index = i

    def __click(self):
        def cc(i):
            def ccc():
                self._select(i)
                onclose()
            return ccc
        chdl = []
        for i, item in enumerate(self.items):
            button = viwid.widgets.button.Button(text=item)
            chdl.append(button)
            button.on_click.append(cc(i))
        box = viwid.widgets.box.Box(orientation=viwid.widgets.box.Orientation.VERTICAL, children=chdl)
        onclose = self.screen.popup(viwid.widgets.frame.Frame(item=box),
                                    alignment=viwid.screen.RootAlignment(
                                        viwid.screen.AnchorRootAlignmentPositioning(self),
                                        viwid.screen.AnchorRootAlignmentPositioning(self),
                                        viwid.screen.AutoRootAlignmentSizing(),
                                        viwid.screen.AutoRootAlignmentSizing()
                                    ))
        # box.children = chdl
