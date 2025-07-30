#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve


class Model(klovve.Model):

    entries = klovve.ListProperty()

    message = klovve.Property(default="")

    began_at = klovve.Property()

    ended_at = klovve.Property()

    only_single_time = klovve.Property(default=False)

    only_verbose = klovve.Property(default=False)

    @klovve.ComputedProperty
    def began_at__text(self) -> str:
        return _time_text(self.began_at)

    @klovve.ComputedProperty
    def ended_at__text(self) -> str:
        if self.only_single_time:
            return ""
        return _time_text(self.ended_at) or (5 * " ･")


class View(klovve.BaseView[Model]):
    pass


def _time_text(d):
    if not d:
        return ""
    return d.strftime("%X")
