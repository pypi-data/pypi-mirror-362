#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import gc
import threading
import time
import weakref
import datetime


class _Memory:

    def __init__(self):
        self.__lock = threading.Lock()
        self.__counters = {}
        self.__counters2 = {}

    def __change_counter(self, kind: str, by: int) -> None:
        with self.__lock:
            self.__counters[kind] = self.__counters.get(kind, 0) + by
            self.__counters2[kind] = self.__counters2.get(kind, 0) + max(0, by)

    def __increment_counter(self, kind: str) -> None:
        self.__change_counter(kind, 1)

    def __decrement_counter(self, kind: str) -> None:
        self.__change_counter(kind, -1)

    @property
    def current(self):
        with self.__lock:
            return dict(self.__counters)

    @property
    def since_startup(self):
        with self.__lock:
            return dict(self.__counters2)        

    def new_object_created(self, obj, kind: str):
        self.__increment_counter(kind)
        weakref.finalize(obj, lambda: self.__decrement_counter(kind))


memory = _Memory()


def _print_loop():  # TODO
    return  # TODO
    while True:
        time.sleep(2*60)
        gc.collect()
        print("\n", datetime.datetime.now())
        print("/-- In memory ----------------------")
        memory_counters = memory.current
        kinds = sorted(memory_counters.keys())
        for kind in kinds:
            print(f"| Number of '{kind}'s: {memory_counters[kind]}")
        print("+-- Created since startup ----------")
        memory_counters = memory.since_startup
        kinds = sorted(memory_counters.keys())
        for kind in kinds:
            print(f"| Number of '{kind}'s: {memory_counters[kind]}")
        print("\\-----------------------------------\n")


threading.Thread(target=_print_loop, daemon=True).start()
