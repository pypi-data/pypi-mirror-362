#  SPDX-FileCopyrightText: © 2021 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve


class Model(klovve.Model):

    items = klovve.ListProperty()

    selected_item = klovve.Property()

    body = klovve.Property()

    item_label_func = klovve.Property()

    list_actions = klovve.ListProperty()

    item_actions = klovve.ListProperty()

    aux_controls = klovve.ListProperty()


class View(klovve.ComposedView[Model]):

    def compose(self):
        pieces, props = self.make_view()
        return pieces.split(
            item1=pieces.list(
                items=props(twoway=False).items,   # TODO list bindings?!
                selected_item=props.selected_item,
                list_actions=props(twoway=False).list_actions,
                item_actions=props(twoway=False).item_actions,
                item_label_func=props(twoway=False).item_label_func,
                aux_controls=props(twoway=False).aux_controls,
            ),
            item2=props(twoway=False).body,
        )
