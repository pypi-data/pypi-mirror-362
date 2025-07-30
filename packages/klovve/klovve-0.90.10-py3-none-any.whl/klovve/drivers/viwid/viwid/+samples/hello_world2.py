#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import asyncio

import viwid.drivers
import viwid.widgets.button
import viwid.widgets.entry
import viwid.widgets.label
import viwid.widgets.box
import viwid.widgets.widget


if __name__ == "__main__":
    driver = viwid.drivers.get_driver()
    label1 = viwid.widgets.label.Label(text="0")
    label2 = viwid.widgets.label.Label(text="0")
    label3 = viwid.widgets.label.Label(text="0")

    loop = asyncio.get_event_loop()
    def stick():
        for l in [label1, label2, label3]:
            l.text = str(int(l.text) + 1)
    def tick():
        stick()
        loop.call_later(5, tick)

    driver.add_widget_screen(viwid.widgets.box.Box(
        children=[

            viwid.widgets.box.Box(
                children=[
                    a:=viwid.widgets.button.Button(text="-",
                                                  vertical_sizing_policy=viwid.widgets.widget.Widget.SizingPolicy.EXPAND_GREEDILY,
                                                  horizontal_sizing_policy=viwid.widgets.widget.Widget.SizingPolicy.EXPAND_GREEDILY),
                    b:=viwid.widgets.button.Button(text="-",
                                                  vertical_sizing_policy=viwid.widgets.widget.Widget.SizingPolicy.EXPAND_GREEDILY,
                                                  horizontal_sizing_policy=viwid.widgets.widget.Widget.SizingPolicy.EXPAND_GREEDILY),
                ],
                orientation=viwid.widgets.box.Orientation.HORIZONTAL
            ),
            viwid.widgets.box.Box(
                children=[
                    label1,
                    viwid.widgets.button.Button(text="-",
                                                  vertical_sizing_policy=viwid.widgets.widget.Widget.SizingPolicy.EXPAND_GREEDILY,
                                                  horizontal_sizing_policy=viwid.widgets.widget.Widget.SizingPolicy.EXPAND_GREEDILY),
                    label2,
                    viwid.widgets.button.Button(text="-",
                                                  vertical_sizing_policy=viwid.widgets.widget.Widget.SizingPolicy.EXPAND_GREEDILY,
                                                  horizontal_sizing_policy=viwid.widgets.widget.Widget.SizingPolicy.EXPAND_GREEDILY),
                    label3
                ],
                orientation=viwid.widgets.box.Orientation.HORIZONTAL
            ),
            viwid.widgets.box.Box(
                children=[
                    viwid.widgets.button.Button(text="-",
                                                  vertical_sizing_policy=viwid.widgets.widget.Widget.SizingPolicy.EXPAND_GREEDILY,
                                                  horizontal_sizing_policy=viwid.widgets.widget.Widget.SizingPolicy.EXPAND_GREEDILY),
                    viwid.widgets.button.Button(text="-",
                                                  vertical_sizing_policy=viwid.widgets.widget.Widget.SizingPolicy.EXPAND_GREEDILY,
                                                  horizontal_sizing_policy=viwid.widgets.widget.Widget.SizingPolicy.EXPAND_GREEDILY),
                ],
                orientation=viwid.widgets.box.Orientation.HORIZONTAL
            ),
            viwid.widgets.box.Box(
                children=[
                    viwid.widgets.button.Button(text="-",
                                                  vertical_sizing_policy=viwid.widgets.widget.Widget.SizingPolicy.EXPAND_GREEDILY,
                                                  horizontal_sizing_policy=viwid.widgets.widget.Widget.SizingPolicy.EXPAND_GREEDILY),
                ],
                orientation=viwid.widgets.box.Orientation.HORIZONTAL
            ),
            viwid.widgets.box.Box(
                children=[
                    viwid.widgets.button.Button(text="-",
                                                  vertical_sizing_policy=viwid.widgets.widget.Widget.SizingPolicy.EXPAND_GREEDILY,
                                                  horizontal_sizing_policy=viwid.widgets.widget.Widget.SizingPolicy.EXPAND_GREEDILY),
                    viwid.widgets.button.Button(text="-",
                                                  vertical_sizing_policy=viwid.widgets.widget.Widget.SizingPolicy.EXPAND_GREEDILY,
                                                  horizontal_sizing_policy=viwid.widgets.widget.Widget.SizingPolicy.EXPAND_GREEDILY),
                    viwid.widgets.button.Button(text="-",
                                                  vertical_sizing_policy=viwid.widgets.widget.Widget.SizingPolicy.EXPAND_GREEDILY,
                                                  horizontal_sizing_policy=viwid.widgets.widget.Widget.SizingPolicy.EXPAND_GREEDILY),
                ],
                orientation=viwid.widgets.box.Orientation.HORIZONTAL
            ),
            viwid.widgets.entry.Entry(),
        ],
        orientation=viwid.widgets.box.Orientation.VERTICAL
    ))
    a.on_click.append(stick)
    b.on_click.append(stick)
    async def goo():
        loop.call_later(1, tick)
        await driver.loop.run()
    loop.run_until_complete(goo())
