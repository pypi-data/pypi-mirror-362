#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
"""
Klovve drivers. Part of internal infrastructure. Klovve applications do not need it.
"""
import abc
import asyncio
import importlib.util
import pkgutil
import typing as t

import klovve.view


class Driver(abc.ABC):
    """
    Internal infrastructure functionality that depends on a particular UI provider implementation.
    """

    __driver = None
    __mainloop = None

    @staticmethod
    def get() -> "Driver":
        """
        Return the current driver. It will automatically be created and initialized internally if needed.
        """
        if not Driver.__driver:
            driver_types = []
            for package in ["", "klovve"]:  # TODO same order as in _find_modules ?!
                package_name_prefix = f"{package}." if package else ""
                drivers_spec = importlib.util.find_spec(f"{package_name_prefix}drivers")
                if drivers_spec:
                    for module_info in pkgutil.iter_modules(drivers_spec.submodule_search_locations):
                        try:
                            driver_module = importlib.import_module(f"{package_name_prefix}drivers.{module_info.name}")
                            driver_types.append(driver_module.Driver)
                        except Exception:
                            continue
            driver_types.sort(key=lambda driver_type: driver_type.rank())
            Driver.__driver = driver = driver_types[0]()
            Driver.__mainloop = driver._create_mainloop()
        return Driver.__driver

    @staticmethod
    def mainloop() -> asyncio.AbstractEventLoop:
        """
        Return Klovve's main loop.

        May only be called after the driver is created.
        """
        if Driver.__mainloop is None:
            raise RuntimeError("unable to find Klovve main loop")
        return Driver.__mainloop

    @staticmethod
    @abc.abstractmethod
    def rank() -> float:
        """
        Return the rank number. Drivers with lower rank will be tried to load first.
        """

    @staticmethod
    @abc.abstractmethod
    def name() -> str:
        """
        Return the driver name.
        """

    @abc.abstractmethod
    def show_window(self, window: "klovve.view.BaseView") -> None:
        """
        Show a window.

        :param window: The window to show.
        """

    @abc.abstractmethod
    def _create_mainloop(self) -> asyncio.AbstractEventLoop:
        """
        Create and return a mainloop.
        """

    def view_type(self, name_tuple: t.Iterable[str]) -> type["klovve.View"]:
        """
        Return a view type by name.

        :param name_tuple: The piece name as tuple.
        """
        for kind in [f"drivers.{self.name()}.views", "pieces"]:
            result = _try_find_type_per_name_tuple(name_tuple, kind, "View")
            if result:
                return result
        raise ValueError(f"there is no view type for {'.'.join(name_tuple)}")

    def model_type(self, name_tuple: t.Iterable[str]) -> type["klovve.View"]:
        """
        Return a model type by name.

        :param name_tuple: The piece name as tuple.
        """
        for kind in [f"drivers.{self.name()}.views", "pieces"]:
            result = _try_find_type_per_name_tuple(name_tuple, kind, "Model")
            if result:
                return result
        raise ValueError(f"there is no model type for {'.'.join(name_tuple)}")


def _try_find_type_per_name_tuple(name_tuple: t.Iterable[str], kind: str, typename: str):
    for module_name in _find_modules(name_tuple, kind):
        kind_type = _try_find_type_in_module(module_name, typename)
        if kind_type:
            return kind_type


def _try_find_type_in_module(module_name: str, typename: str):
    try:
        return getattr(importlib.import_module(module_name), typename, None)
    except ImportError:
        return


def _find_modules(name_tuple: t.Iterable[str], kind: str):
    yield f"klovve.{kind}." + ".".join(name_tuple)
    for i in range(len(tuple(name_tuple))):
        package_name_end = ".".join([*name_tuple[:i], kind, *name_tuple[i:]])
        yield package_name_end
