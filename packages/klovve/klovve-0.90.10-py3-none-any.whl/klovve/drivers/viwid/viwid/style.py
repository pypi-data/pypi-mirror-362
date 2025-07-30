#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only


class StyleAtom:

    def __init__(self, *, foreground, background=None):
        self.foreground = foreground
        self.background = background


class ClassStyle:

    def __init__(self, *, normal: StyleAtom, focussed: StyleAtom, disabled: StyleAtom):
        self.normal = normal
        self.focussed = focussed
        self.disabled = disabled


class RootStyle:

    def __init__(self, *, root: ClassStyle, plain: ClassStyle, control: ClassStyle, entry: ClassStyle, list: ClassStyle,
                 list_item: ClassStyle, selected: ClassStyle, progress_done: ClassStyle, progress_not_done: ClassStyle):
        self.root = root
        self.plain = plain
        self.control = control
        self.entry = entry
        self.list = list
        self.list_item = list_item
        self.selected = selected
        self.progress_done = progress_done
        self.progress_not_done = progress_not_done


class Style:

    def __init__(self, *, main: RootStyle, popup: RootStyle):
        self.main = main
        self.popup = popup


DEFAULT_STYLE = Style(
    main=RootStyle(
        root=ClassStyle(
            normal=StyleAtom(
                foreground="#111",
                background="#fff",
            ),
            focussed=StyleAtom(
                foreground="#111",
                background="#eff #0ff",
            ),
            disabled=StyleAtom(
                foreground="#ff0",
                background="#fff",
            ),
        ),
        plain=ClassStyle(
            normal=StyleAtom(
                foreground="#111",
            ),
            focussed=StyleAtom(
                foreground="#111",
            ),
            disabled=StyleAtom(
                foreground="#ff0",
            ),
        ),
        control=ClassStyle(
            normal=StyleAtom(
                foreground="#fff",
                background="#00c",
            ),
            focussed=StyleAtom(
                foreground="#fff",
                background="#077",
            ),
            disabled=StyleAtom(
                foreground="#ff0",
                background="#f0f",
            ),
        ),
        entry=ClassStyle(
            normal=StyleAtom(
                foreground="#fff",
                background="#00c",
            ),
            focussed=StyleAtom(
                foreground="#fff",
                background="#077",
            ),
            disabled=StyleAtom(
                foreground="#ff0",
                background="#f0f",
            ),
        ),
        list=ClassStyle(
            normal=StyleAtom(
                foreground="#000",
                background="#ddd",
            ),
            focussed=StyleAtom(
                foreground="#111",
                background="#eff #0ff",
            ),
            disabled=StyleAtom(
                foreground="#ff0",
            ),
        ),
        list_item=ClassStyle(
            normal=StyleAtom(
                foreground="#000",
            ),
            focussed=StyleAtom(
                foreground="#fff",
                background="#00c",
            ),
            disabled=StyleAtom(
                foreground="#ff0",
            ),
        ),
        selected=ClassStyle(
            normal=StyleAtom(
                foreground="#000",
                background="#00c",
            ),
            focussed=StyleAtom(
                foreground="#fff",
                background="#00c",
            ),
            disabled=StyleAtom(
                foreground="#111",
                background="#eff #0ff",
            ),
        ),
        progress_done=ClassStyle(
            normal=StyleAtom(
                foreground="#000",
                background="#00f",
            ),
            focussed=StyleAtom(
                foreground="#fff",
                background="#00c",
            ),
            disabled=StyleAtom(
                foreground=1,
                background=1,
            ),
        ),
        progress_not_done=ClassStyle(
            normal=StyleAtom(
                foreground="#000 #fff",
                background="#ccc #000",
            ),
            focussed=StyleAtom(
                foreground="#fff",
                background="#00c",
            ),
            disabled=StyleAtom(
                foreground=1,
                background=1,
            ),
        ),
    ),
    popup=RootStyle(
        root=ClassStyle(
            normal=StyleAtom(
                foreground="#fff",
                background="#44f",
            ),
            focussed=StyleAtom(
                foreground=1,
                background=1,
            ),
            disabled=StyleAtom(
                foreground=1,
                background=1,
            ),
        ),
        plain=ClassStyle(
            normal=StyleAtom(
                foreground="#fff",
            ),
            focussed=StyleAtom(
                foreground="#fff",
            ),
            disabled=StyleAtom(
                foreground=1,
            ),
        ),
        control=ClassStyle(
            normal=StyleAtom(
                foreground="#fff",
                background="#00c",
            ),
            focussed=StyleAtom(
                foreground="#fff",
                background="#077",
            ),
            disabled=StyleAtom(
                foreground=1,
                background=1,
            ),
        ),
        entry=ClassStyle(
            normal=StyleAtom(
                foreground="#fff",
                background="#00c",
            ),
            focussed=StyleAtom(
                foreground="#fff",
                background="#077",
            ),
            disabled=StyleAtom(
                foreground=1,
                background=1,
            ),
        ),
        list=ClassStyle(
            normal=StyleAtom(
                foreground="#000",
                background="#ddd",
            ),
            focussed=StyleAtom(
                foreground=1,
                background=1,
            ),
            disabled=StyleAtom(
                foreground=1,
                background=1,
            ),
        ),
        list_item=ClassStyle(
            normal=StyleAtom(
                foreground="#000",
            ),
            focussed=StyleAtom(
                foreground="#fff",
                background="#00c",
            ),
            disabled=StyleAtom(
                foreground=1,
                background=1,
            ),
        ),
        selected=ClassStyle(
            normal=StyleAtom(
                foreground="#000",
                background="#00c",
            ),
            focussed=StyleAtom(
                foreground="#fff",
                background="#00c",
            ),
            disabled=StyleAtom(
                foreground=1,
                background=1,
            ),
        ),
        progress_done=ClassStyle(
            normal=StyleAtom(
                foreground="#000",
                background="#00f",
            ),
            focussed=StyleAtom(
                foreground="#fff",
                background="#00c",
            ),
            disabled=StyleAtom(
                foreground=1,
                background=1,
            ),
        ),
        progress_not_done=ClassStyle(
            normal=StyleAtom(
                foreground="#000 #fff",
                background="#ccc #000",
            ),
            focussed=StyleAtom(
                foreground="#fff",
                background="#00c",
            ),
            disabled=StyleAtom(
                foreground=1,
                background=1,
            ),
        ),
    ),
)
