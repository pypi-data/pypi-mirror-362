#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
"""
:py:class:`Application` type and some application level utilities.
"""
import asyncio
import functools
import inspect
import threading
import time
import typing as t

import klovve.app.context
import klovve.drivers
import klovve.view.tree


#: View specification type (for type decoration purposes). A view specification defines the application window (what it
#: contains and how it behaves) by a function that gets a view factory as input and returns the view tree node of the
#: application window.
_TViewSpec = t.Callable[["klovve.view.tree.ViewFactory"], "klovve.view.tree.ViewTreeNode"]


def create_app(view_spec: _TViewSpec) -> "Application":
    """
    Create and return a Klovve application, described by a view specification, but not start it yet.

    :param view_spec: The application's view specification.
    """
    return Application(driver=klovve.drivers.Driver.get(), view_spec=view_spec)


class Application:
    """
    A Klovve application. Each instance represents one (potential) running application instance, i.e. one window that
    actually exists somewhere on the screen as soon as it is started.
    """

    __running_apps = []

    __running_apps_changed_event__internal = None

    def __init__(self, *, driver: "klovve.drivers.Driver", view_spec: _TViewSpec):
        """
        :param driver: The driver to use.
        :param view_spec: The view specification for the application's `window`.
        """
        self.__driver = driver
        self.__view_spec = view_spec

    @staticmethod
    def __running_apps_changed_event() -> asyncio.Event:
        verify_correct_thread()
        if not Application.__running_apps_changed_event__internal:
            Application.__running_apps_changed_event__internal = asyncio.Event()
        return Application.__running_apps_changed_event__internal

    async def start(self) -> None:
        """
        Start the application.

        Must be called from inside the Klovve mainloop. Returns directly after starting (non-blocking). Afterwards,
        until it gets closed, :py:meth:`sleep_until_stopped` will sleep and :py:attr:`is_running` will be `True`.
        """
        verify_correct_thread()

        Application.__running_apps.append(self)
        Application.__running_apps_changed_event().set()

        view_factory = klovve.view.tree.ViewFactory(self.__driver)
        window = self.__view_spec(view_factory).view()

        self._view = window  # TODO
        window.native()
        ww = window._ComposedView__result._model.item.view()
        self.__driver.show_window(ww)

        @klovve.reaction(owner=window)
        def _():
            nonlocal ww
            if ww and ww._model.is_closed:
                Application.__running_apps.remove(self)
                Application.__running_apps_changed_event().set()
                ww = None  # TODO mem

    @property
    def is_running(self) -> bool:  # TODO make it a reactive property?
        """
        Whether this application is currently running.
        """
        return self in Application.__running_apps

    async def sleep_until_stopped(self) -> None:
        """
        Wait until the application is stopped. Also return if it was not even started yet.

        Must be called from inside the Klovve mainloop.
        """
        verify_correct_thread()

        while self.is_running:
            await Application.__running_apps_changed_event().wait()
            Application.__running_apps_changed_event().clear()

    def run(self) -> None:
        """
        Run the application and wait until it is closed.

        This is only allowed to be called in the main thread, and when no `asyncio` event loop is currently running in
        that thread. In particular, it is not allowed to be called when another Klovve application is already running in
        that process. For running multiple applications, use :py:meth:`start` and maybe :py:meth:`sleep_until_stopped`
        instead.
        """
        verify_correct_thread()

        try:
            if asyncio.get_running_loop():
                raise ProgramError("there is already a running asyncio event loop")
        except RuntimeError:
            pass

        async def do():
            await self.start()
            while len(Application.__running_apps) > 0:
                await Application.__running_apps_changed_event().wait()
                Application.__running_apps_changed_event().clear()

        mainloop().run_until_complete(do())


def call_maybe_async_func(func: t.Callable, *args, **kwargs) -> t.Awaitable:
    """
    Start running the input function (may be async or normal) in an async way on the Klovve mainloop.

    :param func: The function to call. May be an async function, or a usual, non-async one.
    :param args: Arguments to pass to the function.
    :param kwargs: Keyword arguments to pass to the function.
    """
    result = func(*args, **kwargs)

    if inspect.isawaitable(result):
        return mainloop().create_task(result)
    else:
        future = mainloop().create_future()
        future.set_result(result)
        return future


def mainloop() -> asyncio.AbstractEventLoop:
    """
    Return the mainloop.
    """
    return klovve.drivers.Driver.mainloop()


def in_mainloop(func: t.Callable) -> t.Callable:
    """
    Function decorator that dispatches function execution to the mainloop.

    :param func: The function to call inside the mainloop.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result, exception, result_arrived = None, None, False

        try:
            current_loop = asyncio.get_running_loop()
        except RuntimeError:
            current_loop = None

        if current_loop and current_loop is mainloop():
            return func(*args, **kwargs)

        def inner_func():
            nonlocal result, exception, result_arrived
            try:
                result = func(*args, **kwargs)
            except Exception as ex:
                exception = ex
            result_arrived = True
        mainloop().call_soon_threadsafe(inner_func)

        while not result_arrived:
            time.sleep(0.05)  # TODO
        if exception:
            raise exception
        return result

    return wrapper


class MainloopObjectProxy:
    """
    Simple proxy object that is wrapped around another one, ensuring that all interactions with it take place inside the
    mainloop.
    """

    def __init__(self, obj):
        self.__obj = obj

    def __getattr__(self, item):

        if threading.current_thread() == threading.main_thread():
            return getattr(self.__obj, item)

        def getter():
            value = getattr(self.__obj, item)

            if callable(value):
                def func_wrapper(*args, **kwargs):
                    return in_mainloop(lambda: value(*args, **kwargs))()
                return func_wrapper

            return value
        return in_mainloop(getter)()

    def __setattr__(self, key, value):
        if key == f"_{type(self).__name__}__obj":
            super().__setattr__(key, value)
        else:
            def set_func():
                setattr(self.__obj, key, value)
            if threading.current_thread() == threading.main_thread():
                set_func()
            else:
                in_mainloop(set_func)()


def verify_correct_thread() -> None:
    """
    Raise an exception if called from another thread than the Klovve thread (i.e. the process main thread).
    Otherwise, do nothing.
    """
    if threading.current_thread() != threading.main_thread():
        raise ProgramError("access to Klovve models is not allowed from this thread")


class ProgramError(Exception):
    """
    Internal program errors.
    """
    pass


class ApplicationUnavailableError(RuntimeError):  # TODO use
    """
    Error raised when the application to be started cannot run with any :py:class:`klovve.drivers.Driver` that is
    available on this system.
    """

    def __init__(self):
        super().__init__("This application is not available on your system.")


TAction = t.Callable[["klovve.app.context.ActionContext"], t.Any]
