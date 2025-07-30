#  SPDX-FileCopyrightText: © 2021 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve


class Model(klovve.Model):

    items = klovve.ListProperty()

    selected_items = klovve.ListProperty()

    selected_item = klovve.Property()

    allows_multiselect = klovve.Property()

    list_actions = klovve.ListProperty()

    item_actions = klovve.ListProperty()

    item_label_func = klovve.Property()

    aux_controls = klovve.ListProperty()

    """
    @item_label_func.default
    def item_label_func(self):
        return lambda x: str(x)
    """


class View(klovve.BaseView):

    model: Model
