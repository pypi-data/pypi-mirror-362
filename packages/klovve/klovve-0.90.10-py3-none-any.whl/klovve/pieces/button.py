#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import typing as t

import klovve.app.context


class Model(klovve.Model):

    text: str = klovve.Property(default="")

    action: t.Optional[klovve.app.TAction] = klovve.Property()


class View(klovve.BaseView[Model]):
    pass
