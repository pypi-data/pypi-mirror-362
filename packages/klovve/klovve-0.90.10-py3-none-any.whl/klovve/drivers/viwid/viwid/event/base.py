#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only


class OngoingEvent:

    def __init__(self, name: str):
        self.__name = name
        self.__is_propagation_stopped = False

    @property
    def name(self):
        return self.__name

    @property
    def is_propagation_stopped(self) -> bool:
        return self.__is_propagation_stopped

    def stop_propagation(self) -> None:
        self.__is_propagation_stopped = True
