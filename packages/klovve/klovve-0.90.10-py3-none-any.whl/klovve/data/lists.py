#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
"""
Klovve lists.
"""
import abc
import collections.abc
import typing as t

import klovve.data.observable_value


def _update__default_create_target_object(source_object: t.Any) -> t.Any:
    """
    Default function for target object creation in :py:meth:`List.update`.

    It just returns the source object.

    :param source_object: The source object.
    """
    return source_object


# noinspection PyUnusedLocal
def _update__default_update_target_object(target_object: t.Any, source_object: t.Any) -> None:
    """
    Default function for target object updating in :py:meth:`List.update`.

    It does nothing.

    :param target_object: The target object.
    :param source_object: The source object.
    """
    pass


def _update__default_is_matching_target_object(target_object: t.Any, source_object: t.Any) -> bool:
    """
    Default function for target/source object comparison in :py:meth:`List.update`.

    It compares the objects with the `==` operator.

    :param target_object: The target object.
    :param source_object: The source object.
    """
    return target_object == source_object


class List(collections.abc.MutableSequence, klovve.data.observable_value.CommonObservableValue):
    """
    A list implementation that is observable (with :py:class:`ListObserver` or via
    :py:class:`klovve.data.observable_value.ObservableValueProtocol`) and has some convenience methods.
    """

    def __init__(self, content: t.Iterable = ()):
        super().__init__()
        self.__content = list(content)
        self.__observers: list["ListObserver"] = []

    def __eq__(self, other):
        return (isinstance(other, list) or isinstance(other, List)) and (len(self) == len(other)) \
               and all(self[i] == other[i] for i in range(len(self)))

    def __len__(self):
        return len(self.__content)

    def __getitem__(self, i):
        return self.__content[i]

    def __delitem__(self, i):
        i = self.__correct_index(i)
        del self.__content[i]
        for observer in self.__observers:
            observer.item_removed(i)
        self._trigger_changed()

    def __setitem__(self, i, v):
        i = self.__correct_index(i)
        #TODO not always "replaced" (could be an appending)
        self.__content[i] = v
        for observer in self.__observers:
            observer.item_replaced(i, v)
        self._trigger_changed()

    def insert(self, i, v):
        i = self.__correct_index(i)
        self.__content.insert(i, v)
        for observer in self.__observers:
            observer.item_added(i, v)
        self._trigger_changed()

    def __repr__(self):
        return repr(self.__content)

    def move(self, target_index: int, source_index: int) -> None:
        """
        Move an element.

        :param target_index: The new index.
        :param source_index: The old index.
        """
        target_index = self.__correct_index(target_index)
        source_index = self.__correct_index(source_index)
        self.__content.insert(target_index, self.__content.pop(source_index))
        for observer in self.__observers:
            observer.item_moved(source_index, target_index)
        self._trigger_changed()

    def update(self, source_list: t.Iterable[t.Any], *,
               create_target_object_func: t.Callable[[t.Any], t.Any] = _update__default_create_target_object,
               update_target_object_func: t.Callable[[t.Any, t.Any], None] = _update__default_update_target_object,
               is_matching_target_object_func: t.Callable[[t.Any, t.Any],
                                                          bool] = _update__default_is_matching_target_object):
        """
        Update this list with the content of another one.

        :param source_list: The content to apply to this list.
        :param create_target_object_func: Function that creates a representation for a source object in the target
                                          list. Advanced feature.
        :param update_target_object_func: Function that updates the representation for a source object in the target
                                          list. Advanced feature.
        :param is_matching_target_object_func: Function that checks if a particular object is the representation for
                                               a particular source object in the target list. Advanced feature.
        """
        with klovve.data.deps.pause_refreshing():
            source_list_length = 0
            for i_elem, elem_i in enumerate(source_list):
                source_list_length += 1
                for j_elem in range(i_elem, len(self)):
                    elem_j = self[j_elem]
                    if is_matching_target_object_func(elem_j, elem_i):
                        k_elem = j_elem
                        break
                else:
                    k_elem = -1
                if k_elem >= 0:
                    if k_elem > i_elem:
                        self.move(i_elem, k_elem)
                else:
                    elem_j = create_target_object_func(elem_i)
                    self.insert(i_elem, elem_j)
                update_target_object_func(elem_j, elem_i)
            for _ in range(len(self) - source_list_length):
                self.pop()

    def _add_observer(self, observer: "ListObserver", *, initialize: bool = True) -> None:
        """
        Attach a :py:class:`ListObserver` to this list.

        For a model's list property, you have to use :py:meth:`klovve.data.model.Model.add_list_observer` instead.

        :param observer: The observer to attach.
        :param initialize: Whether to initialize the observer with the current content.
        """
        self.__observers.append(observer)
        if initialize:
            for index, item in enumerate(self.__content):
                observer.item_added(index, item)

    def _remove_observer(self, observer: "ListObserver") -> None:
        """
        Detach a :py:class:`ListObserver` from this list.

        For a model's list property, you have to use TODO instead.

        :param observer: The observer to detach.
        """
        self.__observers.append(observer)

    def __correct_index(self, i: int) -> int:
        if i < 0:
            i += len(self.__content)
        return i


class ListObserver(abc.ABC):  # TODO cooperate with _defer_value_propagation
    """
    Abstract base class for objects that can listen to changes on a :py:class:`List`.
    """

    @abc.abstractmethod
    def item_added(self, index: int, item: object) -> None:
        """
        Called when an item was added to the observed list.

        :param index: The position where the new item was inserted.
        :param item: The new item.
        """

    @abc.abstractmethod
    def item_moved(self, from_index: int, to_index: int) -> None:
        """
        Called when an item was moved inside the observed list.

        :param from_index: The position of the element that was moved.
        :param to_index: The new position of the moved element.
        """

    @abc.abstractmethod
    def item_removed(self, index: int) -> None:
        """
        Called when an item was removed from the observed list.

        :param index: The position of the item that was removed.
        """

    def item_replaced(self, index, item) -> None:
        """
        Called when an item was replaced by another one in the observed list.

        :param index: The position where the item was replaced.
        :param item: The new item.
        """
        self.item_removed(index)
        self.item_added(index, item)
