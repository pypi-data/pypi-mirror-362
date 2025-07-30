#  SPDX-FileCopyrightText: © 2021 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve.pieces.interact


class Model(klovve.pieces.interact.Model):

    message = klovve.Property(default="")

    suggestion = klovve.Property(default="")


class View(klovve.ComposedView[Model]):

    class TModel(klovve.Model):  # TODO
        value = klovve.Property(default="")

    def compose(self):
        pieces, props = self.make_view()
        answer = View.TModel()
        @klovve.reaction(owner=self)
        def _():
            answer.value = self.model.suggestion
        # klovve.data.bind(answer, self.model.suggestion, one_way=True)
        linefield = pieces.text_field(text=props(model=answer).value)
        return pieces.interact.abstract(
            message=props.message,
            inner_view=linefield,
            triggers=["OK", "Cancel"],
            answer=props.answer,
            is_answered=props.is_answered,
            get_answer_func=lambda i: (answer.value if (i == 0) else None)
        )
