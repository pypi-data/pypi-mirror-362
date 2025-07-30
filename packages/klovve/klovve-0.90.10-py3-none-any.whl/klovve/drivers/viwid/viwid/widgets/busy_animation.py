#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import asyncio
import viwid.widgets.label


class BusyAnimation(viwid.widgets.label.Label):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__i = -1
        self.__next()

    def __next(self):
        x = "\\|/-"
        self.__i = (self.__i + 1) % len(x)
        self.text = x[self.__i]
        asyncio.get_running_loop().call_later(0.5, self.__next)  # TODO 0.125
