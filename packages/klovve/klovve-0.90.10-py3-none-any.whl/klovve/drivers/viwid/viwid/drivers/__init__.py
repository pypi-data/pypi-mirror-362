#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import viwid.drivers.driver


_driver = None


def get_driver(event_loop=None) -> "viwid.drivers.driver.Driver":
    global _driver
    if not _driver:
        import viwid.drivers.curses as cursesdriver
        _driver = cursesdriver.Driver(event_loop)
    return _driver
