#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only

#TODO move to __init__ ?!

import klovve.pieces.interact


class Model(klovve.pieces.interact.Model):

    message = klovve.Property()

    inner_view = klovve.Property()

    get_answer_func = klovve.Property(default=lambda: (lambda i: i))

    triggers = klovve.Property(default=lambda: [])  # TODO rename


class View(klovve.BaseView[Model]):
    pass
