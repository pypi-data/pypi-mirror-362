#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
"""
Dependency tracking for model properties.

Klovve applications typically do not need anything from here.
"""
import abc
import contextlib
import contextvars
import typing as t


#: :meta private:
#: A tuple that refers to a particular property from a particular object at a particular point in time (by a version
#: number).
#: Internally used for dependency tracking.
_TDependencyTuple = tuple["DependencySubject", "PropertyBase", int]


#: :meta private:
#: Context variable that gets filled with all dependencies for a particular property, while it is computed.
#: Very often property computations happen in a nested way. While a particular property gets computed, another property
#: (from the same or another object) might be needed, so this one gets computed before the outer computation can
#: continue. Whenever that happens, this list only contains the dependencies for the current innermost computation.
#: Once that is finished, it will again contain the dependencies of the 'outer' computation.
_current_compute_dependencies: contextvars.ContextVar[
    t.Optional[list[_TDependencyTuple]]] = \
    contextvars.ContextVar("_current_compute_dependencies", default=None)


@contextlib.contextmanager
def no_dependency_tracking() -> t.ContextManager[None]:
    """
    Disable dependency tracking of the current computation for a code block.

    Use it for a :code:`with` statement. Model property accesses do not count as a dependency in that :code:`with`
    block.

    It will not influence dependency tracking for other computations inside yours (i.e. if you access a computed
    property, the dependency tracking of this one will not break).
    """
    currently_computing_token = _current_compute_dependencies.set(None)
    try:
        yield
    finally:
        _current_compute_dependencies.reset(currently_computing_token)


#: :meta private:
#: Counts how many :py:func:`pause_refreshing` blocks exist on the current stack. If it is larger than 0, refreshing is
#: considered to be paused.
_defer_value_propagation = 0
#: :meta private:
#: Context variable that gets filled with all properties that need to be propagated to its dependants later, because
#: a :py:func:`pause_refreshing` is executing at the current moment.
_defer_value_propagation_for: t.Optional[list[tuple["DependencySubject", "PropertyBase"]]] = None


# noinspection PyProtectedMember
@contextlib.contextmanager
def pause_refreshing() -> t.ContextManager[None]:
    """
    Defers the automatic refreshes on model property changes for a code block and applies them afterward.

    Use it for a :code:`with` statement. Model property modifications do not instantly lead to updates on depending
    properties in that :code:`with` block.

    Computed properties will always return the right value on access nevertheless, and not an outdated one.
    """
    global _defer_value_propagation, _defer_value_propagation_for
    if _defer_value_propagation == 0:
        _defer_value_propagation_for = []
    _defer_value_propagation += 1
    try:
        yield
    finally:
        _defer_value_propagation -= 1
        if _defer_value_propagation == 0:
            changed_values = list(dict.fromkeys(_defer_value_propagation_for))
            _defer_value_propagation_for = None
            for obj, prop in changed_values:
                obj._trigger_changed(prop)


class PropertyBase:
    """
    Base class for properties on dependency trackable objects.
    This is mostly a marker, TODO.
    """


class DependencySubject(abc.ABC):
    """
    Base class for objects that can attend on dependency tracking.

    For details, read :py:class:`klovve.data.model.PropertyBase` as well.
    """

    @abc.abstractmethod
    def _flush_dependency_handlers(self, prop: "PropertyBase") -> None:
        """
        Remove all change handlers on any object and property which handle the dependency of a particular property.
        Afterward, all change handlers anywhere that would trigger the computation of `prop` are removed.
        This method is usually called just before the dependencies of `prop` are determined again, i.e. just before its
        computation.

        :param prop: The property to consider.
        """

    @abc.abstractmethod
    def _get_dependencies(self, prop: "PropertyBase") -> t.Iterable[_TDependencyTuple]:
        """
        Return all dependencies of a particular property.

        :param prop: The property to consider.
        """

    @abc.abstractmethod
    def _set_dependencies(self, prop: "PropertyBase",
                          new_dependencies: t.Iterable[_TDependencyTuple]) -> None:
        """
        Set the dependencies of a particular property and register change handlers for each one, so `prop` gets
        recomputed whenever the value of a dependency changed.

        :param prop: The property to consider.
        :param new_dependencies: prop's new dependencies.
        """

    @abc.abstractmethod
    def _available_version(self, prop: "PropertyBase") -> int:
        """
        Return which version of `prop` is currently available (i.e. is stored in `__values`).

        :param prop: The property to consider.
        """

    @abc.abstractmethod
    def _add_changed_handler(self, prop: "PropertyBase", func: t.Callable[[], None]) -> None:
        """
        Add a changed handler for a particular property, as a weak reference, which automatically gets removed when
        garbage-collected.

        See also :py:meth:`_remove_changed_handler`.

        :param prop: The property to add a changed handler for.
        :param func: The changed handler.
        """

    def _remove_changed_handler(self, prop: "PropertyBase", func: t.Callable[[], None]) -> None:
        """
        Remove a changed handler for a particular property.

        :param prop: The property to remove a changed handler from.
        :param func: The changed handler.
        """

    # noinspection PyProtectedMember
    @contextlib.contextmanager
    def _detect_dependencies(self, prop: "PropertyBase", *, append: bool = False) -> t.ContextManager[None]:
        """
        Detect dependencies for a code block.

        Use it for a :code:`with` statement.

        :param prop: The property of that object to track dependencies for.
        :param append: If to append dependencies in this block to the known one (instead of replacing them).
        """
        if not append:
            self._flush_dependency_handlers(prop)
        old_current_compute_dependencies = _current_compute_dependencies.set([])
        try:
            yield
        finally:
            new_dependencies = tuple(set(_current_compute_dependencies.get()
                                         + list(self._get_dependencies(prop) if append else ())))
            _current_compute_dependencies.reset(old_current_compute_dependencies)
        self._set_dependencies(prop, new_dependencies)

    def _notify_dependency(self, prop: "PropertyBase") -> None:
        """
        Notify the dependency tracking about a new dependency for the current computation (usually after a property read
        access).

        :param prop: The dependency property in the model.
        """
        current_compute_dependencies = _current_compute_dependencies.get()
        if current_compute_dependencies is not None and (self, prop) not in current_compute_dependencies:  # TODO looks komisch
            current_compute_dependencies.append((self, prop, self._available_version(prop)))

    def _notify_property_value_changed(self, prop: "PropertyBase") -> bool:
        """
        Notify the dependency tracking about the change of a model property and return whether it can proceed
        computations instantly (instead of stopping here, relying on being triggered again later).

        :param prop: The changed property in the model.
        """
        if _defer_value_propagation_for is not None:
            _defer_value_propagation_for.append((self, prop))
            return False
        return True
