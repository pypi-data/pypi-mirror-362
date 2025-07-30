#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import typing as t

import klovve.pieces.log_pager.entry


class Model(klovve.Model):

    entries: list["klovve.pieces.log_pager.entry.Model"] = klovve.ListProperty()

    show_verbose = klovve.Property() #TODO


class View(klovve.BaseView[Model]):
    pass
