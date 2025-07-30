#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve.pieces.tabbed.tab


class Model(klovve.Model):

    items: list["klovve.pieces.tabbed.tab.Model"] = klovve.Property()


class View(klovve.BaseView[Model]):
    pass
