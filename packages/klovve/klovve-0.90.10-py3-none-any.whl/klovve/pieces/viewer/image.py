#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve


class Model(klovve.Model):

    source = klovve.Property(default="")


class View(klovve.BaseView[Model]):
    pass
