#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import typing as t
import klovve


class Model(klovve.Model):

    title: str = klovve.Property(default="12")

    title2: t.Optional[str] = klovve.Property()

    actions = klovve.Property()

    icon = klovve.Property()

    body = klovve.Property()

    closing = klovve.Property()  # TODO computed or readonly

    is_closed = klovve.Property()  # TODO computed or readonly

    name: str = klovve.Property()

    close_func = klovve.Property()


class View(klovve.BaseView):

    model: Model
