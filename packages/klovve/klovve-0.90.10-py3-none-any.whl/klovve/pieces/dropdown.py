#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve


class Model(klovve.Model):

    items: list = klovve.ListProperty()

    selected_item = klovve.Property()

    item_label_func = klovve.Property()


class View(klovve.BaseView):

    model: Model
