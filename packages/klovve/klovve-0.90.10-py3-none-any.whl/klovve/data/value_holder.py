#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import abc
import inspect
import typing as t


# TODO should all that really be view specific?


class ValueHolder(abc.ABC):
    """
    Abstract base class for a single-value container that can be connected to properties of user interface elements;
    either unidirectional or bidirectional.
    """

    @abc.abstractmethod
    def get_value(self) -> t.Any:
        pass

    @abc.abstractmethod
    def set_value(self, value: t.Any) -> None:
        pass

    @abc.abstractmethod
    def is_settable(self) -> bool:
        pass


class OneWayBinding(ValueHolder):
    """
    Connection of a Klovve model object's property, with data flowing only away from it.
    """

    def __init__(self, model, prop_name, converter_in=None, converter_out=None):
        super().__init__()
        self.__model = model
        self.__prop_name = prop_name
        self.__converter_in = converter_in
        self.__converter_out = converter_out

    def get_value(self):
        result = getattr(self.__model, self.__prop_name)
        if self.__converter_in:
            result = self.__converter_in(result)
        return result

    def set_value(self, value):
        if self.is_settable():
            if self.__converter_out:
                value = self.__converter_out(value)
            setattr(self.__model, self.__prop_name, value)

    def is_settable(self):
        return False


class TwoWayBinding(OneWayBinding):
    """
    Connection of a Klovve model object's property, with data flowing in both ways.
    """

    def __init__(self, model, prop_name, converter_in=None, converter_out=None):
        super().__init__(model, prop_name, converter_in, converter_out)

    def is_settable(self):
        return True


class ComputedValue(ValueHolder):

    def __init__(self, func, model, props, pieces):
        super().__init__()
        func_args_count = len(inspect.signature(func).parameters)
        func_args = (model, props, pieces)[:func_args_count]
        self.__func = lambda: func(*func_args)

    def get_value(self):
        return self.__func()

    def set_value(self, value):
        pass

    def is_settable(self):
        return False


class BindFactory:
    """
    Bind factories return value holders like bindings on attribute access.
    The `props` object that you often see in view implementations is a bind factory.
    """

    def __init__(self, model, twoway=True, converter_in=None, converter_out=None):
        self.__model = model
        self.__twoway = twoway
        self.__converter_in = converter_in
        self.__converter_out = converter_out

    def fuh(self, s):
        return s in dir(type(self.__model))
        return hasattr(self.__model, s)

    def __getattr__(self, prop_name):
        if self.__twoway:
            return TwoWayBinding(self.__model, prop_name,
                                                          converter_in=self.__converter_in,
                                                          converter_out=self.__converter_out)
        else:
            return OneWayBinding(self.__model, prop_name,
                                                          converter_in=self.__converter_in,
                                                          converter_out=self.__converter_out)

    def __call__(self, *, model=None, twoway=True, converter_in=None, converter_out=None):
        return BindFactory(model or self.__model, twoway=twoway,
                           converter_in=converter_in or self.__converter_in,
                           converter_out=converter_out or self.__converter_out)
