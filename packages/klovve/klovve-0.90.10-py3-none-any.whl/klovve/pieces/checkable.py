#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve


class Model(klovve.Model):

    text: str = klovve.Property(default="")

    is_checked: bool = klovve.Property(default=False)


class View(klovve.BaseView):

    model: Model
