#  SPDX-FileCopyrightText: © 2021 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve.pieces.interact


class Model(klovve.pieces.interact.Model):

    message = klovve.Property()

    triggers = klovve.Property()  # TODO rename


class View(klovve.ComposedView[Model]):

    def compose(self):
        pieces, props = self.make_view()
        return pieces.interact.abstract(
            message=props.message,
            triggers=props.triggers,
            answer=props.answer,
            is_answered=props.is_answered,
            get_answer_func=lambda i: (self.model.triggers[tuple(self.model.triggers.keys())[i]] if isinstance(self.model.triggers, dict) else i),
        )
