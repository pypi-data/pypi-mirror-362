#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import enum
import klovve


class Model(klovve.Model):

    class State(enum.Enum):
        BUSY = enum.auto()
        SUCCESSFUL = enum.auto()
        SUCCESSFUL_WITH_WARNING = enum.auto()
        FAILED = enum.auto()

    title = klovve.Property(default="12")

    actions = klovve.ListProperty()

    progress = klovve.Property()

    body = klovve.Property()

    state = klovve.Property()

    title_secondary_items = klovve.ListProperty()


class View(klovve.BaseView[Model]):
    pass
