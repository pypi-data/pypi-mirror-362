#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import typing as t


@t.runtime_checkable
class ObservableValueProtocol(t.Protocol):
    """
    Protocol for an observable value. Observable values can be monitored by the Klovve model infrastructure, so it can
    refresh models (e.g. computed properties) not only when property values get reassigned, but also when it points to
    a mutable object (which implements this protocol) and the object _content_ changes.

    This is used for lists (see list properties), but could be used for any kind of mutable objects that you want to
    assign to Klovve properties (although, whenever you can, you should define it as a Klovve model class instead, which
    gives you all that for free).
    """

    def _trigger_changed(self) -> None:
        """
        Process a change (i.e. maybe recompute other property values, ...).

        Call this from inside your observable class whenever the content has been changed.
        """

    def add_changed_handler(self, func: t.Callable[[], None]) -> None:
        """
        Add a change handler. It will be called for any subsequent changes, until :py:meth:`remove_changed_handler` is
        used.

        :param func: The change handler to add.
        """

    def remove_changed_handler(self, func: t.Callable[[], None]) -> None:
        """
        Remove a change handler.

        :param func: The change handler to remove.
        """


class CommonObservableValue(ObservableValueProtocol):
    """
    Basic implementation for the observable value protocol.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__changed_handlers = []

    def _trigger_changed(self):
        for changed_handler in self.__changed_handlers:
            changed_handler()

    def add_changed_handler(self, func):
        self.__changed_handlers.append(func)

    def remove_changed_handler(self, func):
        self.__changed_handlers.remove(func)
