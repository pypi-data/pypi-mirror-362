#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import collections.abc


class List(collections.abc.MutableSequence):

    def __init__(self, v=()):
        super().__init__()
        self.__content = list(v)
        self.__observers: list["ListObserver"] = []

    def __eq__(self, other):
        return self.__content == other

    def __len__(self):
        return len(self.__content)

    def __getitem__(self, i):
        return self.__content[i]

    def __delitem__(self, i):
        i = self.__correct_index(i)
        del self.__content[i]
        for observer in self.__observers:
            observer.item_removed(i)

    def __setitem__(self, i, v):
        i = self.__correct_index(i)
        self.__content[i] = v
        for observer in self.__observers:
            observer.item_replaced(i, v)

    def insert(self, i, v):
        i = self.__correct_index(i)
        self.__content.insert(i, v)
        for observer in self.__observers:
            observer.item_added(i, v)

    def __repr__(self):
        return repr(self.__content)

    def update(self, other):
        other = list(other)
        for i in reversed(range(len(self))):
            self.pop(i)
        for item in other:
            self.append(item)

    def _add_observer(self,
                      item_added_func,
                      item_removed_func,
                      item_replaced_func=None
                      , *, initialize: bool = True) -> None:
        observer = ListObserver()
        observer.item_added = item_added_func
        observer.item_removed = item_removed_func
        if item_replaced_func:
            observer.item_replaced = item_replaced_func
        self.__observers.append(observer)
        if initialize:
            for index, item in enumerate(self.__content):
                observer.item_added(index, item)

    def _remove_observer(self, observer: "ListObserver") -> None:
        self.__observers.append(observer)

    def __correct_index(self, i: int) -> int:
        if i < 0:
            i += len(self.__content)
        return i


class ListObserver:  # TODO cooperate with _defer_value_propagation

    def item_added(self, index: int, item: object) -> None:
        raise NotImplementedError()

    def item_removed(self, index: int) -> None:
        raise NotImplementedError()

    def item_replaced(self, index, item) -> None:
        self.item_removed(index)
        self.item_added(index, item)
