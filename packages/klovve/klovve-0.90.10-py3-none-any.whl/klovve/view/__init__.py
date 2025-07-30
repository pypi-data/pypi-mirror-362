#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import abc
import typing as t

import klovve.debug
import klovve.data.model
import klovve.data.value_holder
import klovve.view.tree

if t.TYPE_CHECKING:
    import klovve.drivers


_TGoo = t.TypeVar("_TGoo", bound="klovve.data.model.Model")#TODO


class View(abc.ABC):
    """
    A view piece.
    """

    @abc.abstractmethod
    def native(self) -> object:
        """
        Return the native representation for this view.
        Internally uses :py:meth:`create_native` for creating it, but then keeps that result for later calls.
        """


class BaseView(t.Generic[_TGoo], klovve.data.model.Model, View):
    """
    Base class for a view piece.
    """

    def __init__(self, model: _TGoo, view_factory: "klovve.view.tree.ViewFactory"):
        super().__init__()
        klovve.debug.memory.new_object_created(self, View.__name__)
        self._model: _TGoo = model
        self._view_factory = view_factory
        self.__result = None

    @property
    def model(self) -> "_TGoo":
        return self._model

    class Rambo:

        def __init__(self, a, b):
            self._a = a
            self._b = b
            self.__setattr__ = self.__setattr__X

        def __getattr__(self, item):
            return getattr(self._a if self._a.fuh(item) else self._b, item)

        def __setattr__X(self, key, value):
            raise Exception("TODO not allowed")  # TODO ?!

        def __call__(self, *args, **kwargs):
            return self._b(*args, **kwargs)  # TODO always b ?!
#            return (self._a if self._a.fuh(item) else self._b)

    #TODO here?!
#    def make_view(self) -> tuple["klovve.view.tree.ViewFactory", t.Union["_TGoo", "t.Self"]]:#TODO Intersection
    def make_view(self) -> tuple["klovve.view.tree.ViewFactory", "_TGoo"]:
        return self._view_factory, self.Rambo(klovve.data.value_holder.BindFactory(self), klovve.data.value_holder.BindFactory(self._model))

    def create_native(self) -> object:
        """
        Create a native representation for this view.

        This must be implemented in native views, but is only called internally. See also :py:meth:`native`.
        """
        raise NotImplementedError(f"no view implementation for {type(self).__module__}")

    def native(self):
        """
        Return the native representation for this view.
        Internally uses :py:meth:`create_native` for creating it, but then keeps that result for later calls.
        """
        if not self.__result:
            bind_factory = klovve.data.value_holder.BindFactory(self._model)
            # noinspection PyTypeChecker
            self.__result = self.create_native()
        return self.__result


class ComposedView(BaseView, t.Generic[_TGoo]):
    """
    Base class for a composed view piece, i.e. a view that is not implemented using native UI toolkits, but by
    composing other Klovve view pieces together.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__result = self._view_factory.create_view(("placeholder",))
        self.__tree = None

    def create_native(self):
        @klovve.reaction(owner=self)
        def _ui():
            # noinspection PyTypeChecker
            compo = self.compose() or self._view_factory.create_view(("placeholder",))
            with klovve.data.deps.no_dependency_tracking():
                compo.create_or_update_view(self._model, self.__result, self.__tree)
                self.__tree = compo

        return self.__result.native()

    def compose(self) -> "klovve.view.tree.ViewTreeNode":
        raise NotImplementedError()
