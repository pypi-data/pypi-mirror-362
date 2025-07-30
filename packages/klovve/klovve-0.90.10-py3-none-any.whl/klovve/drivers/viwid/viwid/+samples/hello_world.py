#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import asyncio

import viwid.drivers
import viwid.widgets.label
import viwid.widgets.box


if __name__ == "__main__":
    driver = viwid.drivers.get_driver()
    driver.add_widget_screen(viwid.widgets.box.Box(
        children=[
            viwid.widgets.label.Label(text="Hello,"),
            viwid.widgets.label.Label(text=" World!"),
        ],
        orientation=viwid.widgets.box.Orientation.HORIZONTAL
    ))
    asyncio.get_event_loop().run_until_complete(driver.loop.run())
