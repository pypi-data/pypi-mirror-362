#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
"""
Reactions are a way to define a computation that is repeated automatically whenever depending model values change.
See :py:func:`reaction`.
"""
import typing as t
import uuid

import klovve.data.model


class _ReactionModel(klovve.data.model.Model):
    """
    Artificial model, internally used by :py:func:`reaction`.
    """

    def __init__(self, func):
        super().__init__()
        self._func = func

    def __str__(self):
        return f"<_ReactionModel {self._func.__name__}>"

    def __call__(self):
        return self.value

    @klovve.data.model.ComputedProperty
    def value(self):
        if self._func is None:
            return self._last_val
        try:
            self._last_val = self._func()   #  TODO _last_val weg
        except Delete:
            self._func = None
            # TODO fully delete everything


# noinspection PyProtectedMember
def reaction(*, owner: t.Any,
             initially: klovve.data.model._TGetValueFunc = klovve.data.model._none,
             use_last_value_during_recompute: bool = True
             ) -> t.Callable[[klovve.data.model._TGetValueFunc], _ReactionModel]:
    """
    Define a function to be a reaction. It will automatically get executed when defined, and whenever any depending
    model values change.

    Use it as a function decorator.

    It is similar to a :py:class:`klovve.data.model.ComputedProperty` in a model, but can be defined anywhere,
    which makes them very convenient in some situations.

    :param owner: The object which owns the reaction. The reaction will usually stay alive as long as the owner still
                  exists.
    :param initially: Function which returns the initial value. Only relevant for :code:`async` reactions.
    :param use_last_value_during_recompute: Whether to use the last computed value during re-computation (instead of
                                            setting it back to the initial value meanwhile).
    """
    # noinspection PyProtectedMember
    def decorator(func_):
        if (initially is not klovve.data.model._none) or (not use_last_value_during_recompute):
            class ReactionModelType(_ReactionModel):
                @klovve.data.model.ComputedProperty(initially=initially,
                                                    use_last_value_during_recompute=use_last_value_during_recompute)
                def value(self):
                    return self._func()
        else:
            # noinspection PyPep8Naming
            ReactionModelType = _ReactionModel
        result = ReactionModelType(func_)
        if owner:
            setattr(owner, f"__{str(uuid.uuid4()).replace('-', '_')}", result)  # TODO
        with klovve.data.deps.no_dependency_tracking():
            _ = result.value
        return result

    return decorator


class Delete(Exception):
    pass
