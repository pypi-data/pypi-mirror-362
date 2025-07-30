#  SPDX-FileCopyrightText: © 2021 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve


class Model(klovve.Model):

    side_item = klovve.Property()

    main_item = klovve.Property()


class View(klovve.BaseView):

    model: Model
