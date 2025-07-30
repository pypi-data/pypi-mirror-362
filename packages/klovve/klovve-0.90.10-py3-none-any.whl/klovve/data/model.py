#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
"""
Klovve data models.
"""
import asyncio
import functools
import inspect
import typing as t
import weakref

import klovve.app
import klovve.data.deps
import klovve.data.lists
import klovve.data.observable_value
import klovve.debug


#: Python type for a callable without parameters that returns some value (or not, which is as returning `None`).
_TGetValueFunc = t.Callable[[], t.Any]


def _none() -> None:
    """
    Return :code:`None`.
    """
    return None


#  TODO computed_list_model_property


class Model(klovve.data.deps.DependencySubject):
    """
    Base class for Klovve data models (i.e. view-models).

    As a :py:class:`klovve.data.deps.DependencySubject` it is part of Klovve data dependency tracking with special
    properties defined on it (see :py:class:`Property`, :py:class:`ComputedProperty` and others).
    """

    # noinspection PyProtectedMember
    def __init__(self, **kwargs):
        klovve.debug.memory.new_object_created(self, Model.__name__)
        # TODO.
        self.__values: dict["PropertyBase", object] = {}
        # TODO.
        self.__head_versions: dict["PropertyBase", int] = {}
        # TODO.
        self.__available_versions: dict["PropertyBase", int] = {}
        # Handlers that TODO.
        self.__changed_handlers: dict["PropertyBase", weakref.ReferenceType[t.Callable]] = {}
        # TODO.
        self.__dependencies: dict["PropertyBase", t.Iterable[klovve.data.deps._TDependencyTuple]] = {}
        # Handlers that TODO.
        self.__dependencies_handlers: dict["PropertyBase", tuple[t.Optional[t.Callable],
                                           t.Iterable[klovve.data.deps._TDependencyTuple]]] = {}
        # Handlers that TODO.
        self.__value_changed_handlers: dict["PropertyBase", t.Callable] = {}
        # TODO.
        self.__next_version = 2
        for k, v in kwargs.items():
            setattr(self, k, v)

    def _value(self, prop: "PropertyBase") -> t.Any:
        """
        Return the value for a property.

        It always returns the recent version, i.e. no (synchronous) computation or reaction is still going on for this
        property anymore (even during :py:func:`klovve.deps.pause_refreshing`). There can be async
        computations going on, though, which affect the value later (which should be no problem, as this will just
        lead to a new version of this property and dependants get evaluated again).

        :param prop: The property to fetch the value for.
        """
        do_refresh = self.__head_version(prop) != self._available_version(prop)

        if do_refresh:  # TODO have a while loop here instead?! in dependency-loop situations, it will then either work more correctly, or freeze?
            last_result = self.__values.get(prop, None)
            if isinstance(last_result, klovve.data.observable_value.ObservableValueProtocol) \
                    and (prop in self.__value_changed_handlers):
                last_result.remove_changed_handler(self.__value_changed_handlers.pop(prop))

            self.__compute(prop)

        self._notify_dependency(prop)

        result = self.__values[prop]
        if do_refresh and isinstance(result, klovve.data.observable_value.ObservableValueProtocol):
            trigger_changed = self.__value_changed_handlers[prop] = functools.partial(self._trigger_changed, prop)
            result.add_changed_handler(trigger_changed)
        return result

    def _trigger_changed(self, prop: "PropertyBase") -> None:  # TODO we do not want to implement ObservableValueProtocol here, do we? should we? rename or finish?
        """
        React to a changed value for a particular property, refresh all dependent computed properties, and so on.

        Inside a :py:func:`klovve.deps.pause_refreshing` block, it will do nothing, but just ensure to be called
        again after that block.

        :param prop: The property which value has been changed.
        """
        if not self._notify_property_value_changed(prop):
            return
        changed_handlers = self.__changed_handlers.get(prop, None)
        if changed_handlers:
            for i, changed_handler_ in enumerate(reversed(changed_handlers)):
                changed_handler = changed_handler_()
                if not changed_handler:
                    changed_handlers.pop(i)
                    continue
                changed_handler()

    def _set_value(self, prop: "PropertyBase", value: t.Any) -> None:
        """
        Set a property to a new value and trigger automatic re-computation of dependent values.

        :param prop: The property to set.
        :param value: The new value.
        """
        if (prop in self.__values) and (self.__values[prop] == value) \
                and (not isinstance(self.__values[prop], klovve.data.observable_value.ObservableValueProtocol)):  # TODO ObservableValueProtocol handling here makes sense?!
            return
        self.__values[prop] = value
        self.__head_versions[prop] = self.__available_versions[prop] = self.__next_version
        self.__next_version += 1
        self._trigger_changed(prop)

    # noinspection PyProtectedMember
    def __compute(self, prop: "PropertyBase") -> None:
        """
        Refresh the value for a particular property. This either makes the fresh value directly available, or at least
        triggers async computation to make a fresh value appear as soon as possible.

        :param prop: The property to refresh.
        """
        with self._detect_dependencies(prop):
            new_value = prop._compute(self)
        is_async = inspect.isawaitable(new_value)
        if is_async:
            async def xx():
                with self._detect_dependencies(prop, append=True):
                    new_value_awaited = await new_value
                self._set_value(prop, new_value_awaited)

            if (not prop._use_last_value_during_recompute()) or (prop not in self.__values):
                self._set_value(prop, prop._initially())
            asyncio.get_event_loop().create_task(xx())#TODO keep a reference to it
        else:
            self._set_value(prop, new_value)

    def _add_changed_handler(self, prop, func):
        changed_handlers = self.__changed_handlers.get(prop, None)
        if changed_handlers is None:
            changed_handlers = self.__changed_handlers[prop] = []
        func_weak = weakref.ref(func)
        changed_handlers.append(func_weak)
        weakref.finalize(func, functools.partial(self._remove_changed_handler, prop, func_weak))

    def _remove_changed_handler(self, prop, func):
        changed_handlers = self.__changed_handlers.get(prop, None)
        if changed_handlers:
            for changed_handler_ in list(changed_handlers):
                changed_handler = changed_handler_()
                if not changed_handler or (changed_handler == func):
                    changed_handlers.remove(changed_handler_)

    def _flush_dependency_handlers(self, prop):
        none_tuple = (None, ())
        old_func, old_dependencies = self.__dependencies_handlers.get(prop, none_tuple)
        if old_func:
            for old_dependency_obj, old_dependency_key, _ in old_dependencies:
                old_dependency_obj._remove_changed_handler(old_dependency_key, old_func)
            self.__dependencies_handlers[prop] = none_tuple

    def _get_dependencies(self, prop):
        return self.__dependencies.get(prop, ())

    def _set_dependencies(self, prop, new_dependencies):
        self.__dependencies[prop] = new_dependencies
        recompute = functools.partial(self.__compute, prop)
        for new_dependency_obj, new_dependency_prop_name, _ in new_dependencies:
            new_dependency_obj._add_changed_handler(new_dependency_prop_name, recompute)
        self.__dependencies_handlers[prop] = (recompute, new_dependencies)

    def _available_version(self, prop):
        return self.__available_versions.get(prop, 0)

    def __invalidate(self, prop: "PropertyBase"):
        """
        Mark the current value of a particular property as outdated.
        This does not directly execute any re-computation (but will enforce it on next access).

        :param prop: The property to mark.
        """
        self.__head_versions[prop] = self.__next_version + 1
        self.__next_version += 1

    def __head_version(self, prop: "PropertyBase"):
        """
        Return which version of a particular property is the most recent one. This will automatically be higher than
        the available version if any dependency has changed its value since the last computation of `prop`.

        :param prop: The property to consider.
        """
        dependencies = self.__dependencies.get(prop, ())

        for model, prop_, version in dependencies:
            if version != model.__head_version(prop_):
                self.__invalidate(prop)
                break

        result = self.__head_versions.get(prop, 1)
        return result

    def __call__(self, *args, **kwargs):  # TODO  only helps the ide
        return self


# noinspection PyProtectedMember
class PropertyBase(klovve.data.deps.PropertyBase, property):
    """
    Base class for Klovve properties. They can be like variables (i.e. you can read and write them), or computed, like
    Python properties (i.e. you can read them, but they contain computed values). See subclasses.

    Properties are defined in :py:class:`Model` subclasses. For each instance of those models, a property will carry its
    value, very much like the most basic usage of variables and properties in usual classes.

    On top of bare Python variables and properties, you can directly bind Klovve properties to properties of user
    interface elements, keeping everything up-to-date without any manual plumbing of change handlers or similar.
    """

    def __init__(self):
        super().__init__(self._fget, self._fset)

    def _fget(self, obj):
        """
        Return the property value.

        :param obj: The object to get the value from.
        """
        klovve.app.verify_correct_thread()
        return obj._value(self)

    def _fset(self, obj, value):
        """
        Set the property to a new value.

        :param obj: The object to set the value for.
        :param value: The new value.
        """
        klovve.app.verify_correct_thread()
        obj._set_value(self, value)

    def _compute(self, obj) -> t.Any:
        """
        Compute and return the property value.
        This will execute the value computation if there is any.

        :param obj: The object to compute the value for.
        """
        raise NotImplementedError()

    def _initially(self) -> t.Any:
        return None

    def _use_last_value_during_recompute(self) -> bool:
        return True


# noinspection PyProtectedMember
class Property(PropertyBase):
    """
    A variable-like property (i.e. gettable and settable). If you want to store a list, you should use
    :py:class:`ListProperty` instead (otherwise performance may degrade and the user interface may behave in undesired
    ways).
    """

    def __init__(self, *, default: t.Union[t.Any, t.Callable[[], t.Any]] = _none):
        super().__init__()
        self.__get_default = default if callable(default) else (lambda: default)

    def _compute(self, obj):
        return self.__get_default()  # that's fine, since we just get called on initialization anyway


# noinspection PyProtectedMember
class ListProperty(Property):
    """
    A variable-like property, but containing a list. The list itself cannot be replaced (i.e. not settable), but you
    can modify its content (in the same way as for Python lists and some additional ones; see
    :py:class:`klovve.data.lists.List`).
    """

    def __init__(self, *, default: t.Callable[[], t.Iterable[t.Any]] = lambda: ()):
        super().__init__(default=lambda: klovve.data.lists.List(default()))

    def _fset(self, obj, value):
        klovve.app.verify_correct_thread()
        self._fget(obj).update(value)


# noinspection PyProtectedMember
class _ComputedProperty(PropertyBase):
    """
    A computed property. You will usually define it by means of :py:func:`ComputedProperty`.
    """

    def __init__(self, func, *, initially: _TGetValueFunc, use_last_value_during_recompute: bool):
        super().__init__()
        self._fct = func
        self.__initially = initially
        self.__use_last_value_during_recompute = use_last_value_during_recompute

    def _initially(self):
        return self.__initially()

    def _use_last_value_during_recompute(self):
        return self.__use_last_value_during_recompute

    def _fset(self, obj, value):
        klovve.app.verify_correct_thread()

    def _compute(self, obj):
        return self._fct(obj)


# noinspection PyPep8Naming
def ComputedProperty(func: t.Optional[_TGetValueFunc] = None, *,
                     initially: _TGetValueFunc = _none,
                     use_last_value_during_recompute: bool = True) -> t.Callable[[_TGetValueFunc], _ComputedProperty]:
    """
    Decorate a method to be a computed property.

    :param func: The method (of a :py:class:`Model` subclass) to consider as computed property.
    :param initially: Function that returns the initial value, which this property holds before any computation.
                      This is only relevant if `func` is `async`.
    :param use_last_value_during_recompute: Whether this property should keep the old value during computation (instead
                                            of falling back to the initial value meanwhile).
                                            This is only relevant if `func` is `async`.
    """
    def decorator(func_):
        return _ComputedProperty(func_, initially=initially,
                                 use_last_value_during_recompute=use_last_value_during_recompute)

    return decorator if (func is None) else decorator(func)


def observe_list(model: "Model", prop_name: str, observer: "klovve.data.lists.ListObserver", *,
                 initialize: bool = True) -> None:  # TODO remove observers?!
    """
    Start observing a list (i.e. a value of a :py:class:`ListProperty`).

    :param model: The model object to observe.
    :param prop_name: The name of the list property.
    :param observer: The observer.
    :param initialize: Whether to push the current list content to the observer now.
    """
    with klovve.data.deps.no_dependency_tracking():
        # noinspection PyProtectedMember
        getattr(model, prop_name)._add_observer(observer, initialize=initialize)
