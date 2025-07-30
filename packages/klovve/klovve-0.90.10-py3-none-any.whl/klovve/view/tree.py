#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import asyncio
import typing as t

import klovve.debug
import klovve.data.model
import klovve.data.value_holder
import klovve.view

if t.TYPE_CHECKING:
    import klovve.drivers


class ViewTreeNode:
    """
    Definition for one view item in a view, including the view type, the model, and data TODO.
    As the TODO potentially contains other view nodes (for a view that is composed of smaller pieces), this is a
    hierarchical structure, with the root node specifying your entire user interface.
    """

    def __init__(self, view_factory, name_tuple, model, data: t.Iterable[tuple[str, t.Any]]):
        klovve.debug.memory.new_object_created(self, ViewTreeNode.__name__)
        self.__view_factory = view_factory
        self.__name_tuple = name_tuple
        self.__model = model
        self.__data = dict(data)
        self.__view = None

    def __str__(self):
        return f"<{self.__name_tuple}>" # TODO

    @property
    def name_tuple(self) -> t.Iterable[str]:
        return self.__name_tuple

    @property
    def model(self) -> t.Optional["klovve.Model"]:
        """
        A model, if this view pieces was specified by a model as argument (which is quite unusual).
        """
        return self.__model

    @property
    def data(self) -> dict[str, t.Any]:
        """
        The data specified for this view piece.
        Values will contain fixed values as well as value holders. This potentially includes other view nodes (or lists,
        ... of them).
        """
        return dict(self.__data)

    def view(self) -> "klovve.view.View":
        """
        Return the view specified by this node. This is created on-demand but then cached and re-used.
        """
        if not self.__view:
            zeug = []
            value_holders = []
            rk = {}
            if not self.model:
                for k, v in self.data.items():
                    if isinstance(v, klovve.data.value_holder.ValueHolder):
                        value_holders.append((k, v))
                    else:
                        rk[k] = v
            self.__view = self.__view_factory.create_view(self.name_tuple, model=self.model, **rk)

            for value_holder in value_holders:
                zeug.append(_connect_value_holder(self.__view._model, *value_holder))

            self.__view.__zeug = zeug

        return self.__view

    def create_or_update_view(self, model: "klovve.Model", placeholder, old_tree: "ViewTreeNode"):
        """
        Create the view defined by this node, or update it.

        :param model:
        :param placeholder:
        :param old_tree:
        """

        self.__create_or_update_view(old_tree, self, model, placeholder, "item")

    def __create_or_update_view(self, old_tree: "ViewTreeNode", new_tree: "ViewTreeNode", model: "klovve.Model",
                                parent_view: "klovve.view.View", parent_view_prop_name: str):
        with klovve.data.deps.pause_refreshing(): # TODO xx xxxxx
        #with klovve.data.deps.no_dependency_tracking():

            if (not old_tree) or not hasattr(new_tree, "name_tuple") or not hasattr(old_tree, "name_tuple") or (new_tree.name_tuple != old_tree.name_tuple) or (new_tree.model != old_tree.model):  # TODO EQU  or even  sleutel
                setattr(parent_view._model, parent_view_prop_name, self)
            else:
                existing_view = getattr(parent_view._model, parent_view_prop_name).view()
                zeug = new_tree._zeug = []
                def schit(prop_key, prop_value):
                    zeug.append(_connect_value_holder(existing_view._model, prop_key, prop_value))

                for prop_key, prop_value in new_tree.data.items():  # TODO remove/reset other keys
                    # TODO all odd
                    if isinstance(prop_value, ViewTreeNode):
                        Xold_tree = old_tree.data.get(prop_key, None)
                        self.__create_or_update_view(Xold_tree, prop_value, model, existing_view, prop_key)
                    elif isinstance(prop_value, klovve.data.value_holder.ValueHolder):
                        #asyncio.get_running_loop().call_soon(schit, prop_key, prop_value)
                        zeug.append(_connect_value_holder(existing_view._model, prop_key, prop_value)) #  ?!?!
                    else:
                        setattr(existing_view._model, prop_key, prop_value)


class ViewFactory:
    """
    View factories return view piece factories on attribute access. These create a :py:class:`ViewTreeNode` when called.
    The `pieces` object that you often see in view implementations is a view factory.
    """

    class _Node:

        def __init__(self, view_factory: "ViewFactory", view_name: t.Iterable[str]):
            self.__view_factory = view_factory
            self.__view_name = view_name

        def __getattr__(self, item: str) -> "ViewFactory._Node":
            return ViewFactory._Node(self.__view_factory, (*self.__view_name, item))

        def __call__(self, model_or_model_type=None, /, **kwargs):
            model = model_or_model_type() if isinstance(model_or_model_type, type) else model_or_model_type
            return ViewTreeNode(self.__view_factory, self.__view_name, model, kwargs)

    def create_view(self, name_tuple: t.Iterable[str], /, *, model=None, **kwargs) -> "klovve.view.View":
        model_type = model or self.__driver.model_type(name_tuple)
        if not model_type:
            raise ViewError(f"unable to find the model type for {name_tuple}")
        model = model_type()
        for key, value in kwargs.items():
            setattr(model, key, value)
        return self.__driver.view_type(name_tuple)(model, self)

    def __getattr__(self, item) -> "ViewFactory._Node":
        return ViewFactory._Node(self, (item,))

    def __init__(self, driver: "klovve.drivers.Driver"):
        self.__driver = driver


class ViewError(Exception):
    pass


def _connect_value_holder(target_model: "klovve.Model", target_prop_name: str,
                          value_holder: "klovve.data.value_holder.ValueHolder") -> object:

    @klovve.reaction(owner=None)
    def _handle_to_target():
        value = value_holder.get_value()
        with klovve.data.deps.no_dependency_tracking():
            setattr(target_model, target_prop_name, value)

    @klovve.reaction(owner=_handle_to_target)
    def _handle_from_target():
        if value_holder.is_settable():
            value = getattr(target_model, target_prop_name)
            with klovve.data.deps.no_dependency_tracking():
                value_holder.set_value(value)

    return _handle_to_target
