#  SPDX-FileCopyrightText: © 2021 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve


class Model(klovve.Model):

    items = klovve.ListProperty()  # TODO was Property !!!!!


class View(klovve.BaseView[Model]):
    pass
