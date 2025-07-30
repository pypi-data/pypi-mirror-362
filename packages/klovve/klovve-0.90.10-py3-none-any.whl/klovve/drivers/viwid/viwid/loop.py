#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import asyncio
import typing as t


class Loop:

    def __init__(self, event_loop: t.Optional[asyncio.BaseEventLoop] = None):
        self.__event_loop = event_loop

    @property
    def event_loop(self) -> asyncio.BaseEventLoop:
        return self.__event_loop

    async def run(self) -> None:
        pass
