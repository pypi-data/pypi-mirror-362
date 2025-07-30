#  SPDX-FileCopyrightText: © 2021 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve


class Model(klovve.Model):

    value: float = klovve.Property()

    min_value: float = klovve.Property()

    max_value: float = klovve.Property()

    step_value: float = klovve.Property()


class View(klovve.BaseView):

    model: Model
