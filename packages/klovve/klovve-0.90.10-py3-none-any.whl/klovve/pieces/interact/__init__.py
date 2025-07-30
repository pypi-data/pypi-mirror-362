#  SPDX-FileCopyrightText: © 2021 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import typing as t

import klovve


class Model(klovve.Model):

    answer: t.Any = klovve.Property()

    is_answered: bool = klovve.Property(default=False)

    def set_answer(self, answer):
        self.answer = answer
        self.is_answered = True
