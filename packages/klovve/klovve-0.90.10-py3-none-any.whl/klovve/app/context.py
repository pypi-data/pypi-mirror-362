#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
"""
Contexts are objects with additional info and/or functionality that is available to the application developer for
particular situations (e.g. user interactions).
"""
import abc
import asyncio
import contextlib
import traceback
import typing as t

import klovve.data.model
import klovve.data.reaction
import klovve.view.tree


_TGoo = t.TypeVar("_TGoo", bound="klovve.data.model.Model")#TODO


class ActionContext(t.Generic[_TGoo], abc.ABC):
    """
    Action contexts provide a way to interact with the user by means of dialogs in the execution of an action, e.g.
    after the user has clicked on a button. There is also some more functionality for action execution.
    """

    def __init__(self, pieces):
        self.__pieces = pieces

    @contextlib.asynccontextmanager
    async def error_message_for_exceptions(self, *exception_types):
        """
        If exceptions (of particular types) get raised inside the with-block, a dialog with the exception message will
        be shown to the user.

        :param exception_types: The types to catch.
        """
        try:
            yield
        except Exception as ex:
            if isinstance(ex, exception_types):
                await self.dialog(self.__pieces.interact.message(message=str(ex)))
                traceback.print_exc()#TODO weg
            else:
                raise ex

    @abc.abstractmethod
    async def _create_dialog(self, view: "klovve.view.View", done_future: asyncio.Future):
        """
        TODO
        Create a dialog with the given view content, and wait until `done_future` is done.
        Implemented by subclasses, but not directly used from outside.

        :param view: The view to show in a dialog.
        :param done_future: The future to wait for before closing the dialog again.
        """

    async def dialog(self, view: "klovve.view.tree.ViewTreeNode") -> t.Any:  # TODO closable?!
        """
        Show a dialog to the user and return the answer that the user gave.

        The model of this dialog must have a boolean `is_answered` property that is True once the user has chosen to
        close and continue (maybe via an OK button, or however the view shall behave), and an `answer` property that
        contains the value returned by this function then.

        :param view: The view node that describes the content to show in the dialog. You usually create it with a
                     :py:class:`klovve.view.tree.ViewFactory`.
        """
        done_future = klovve.app.mainloop().create_future()
        view_ = view.view()

        @klovve.reaction(owner=done_future)
        def _():
            print("YY",view_.model.is_answered)
            if view_.model.is_answered:
                done_future.set_result(view_.model.answer)
                raise klovve.data.reaction.Delete()

        return (await asyncio.gather(done_future, self._create_dialog(view_, done_future)))[0]
