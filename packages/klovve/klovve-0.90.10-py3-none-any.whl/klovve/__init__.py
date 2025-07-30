#  SPDX-FileCopyrightText: © 2021 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
"""
Klovve.

Everything needed for a simple Klovve application is in that module. There are more things in various submodules, but
you will rarely, if ever, need them.
"""
import klovve.data.deps

from klovve.app import create_app, ApplicationUnavailableError
from klovve.data.model import Model, Property, ListProperty, ComputedProperty
from klovve.data.lists import ListObserver
from klovve.data.reaction import reaction
from klovve.view import ComposedView, BaseView

"""
TODO

computed observables: auto detect dependencies instead of kwargs?
  
---- ^^ DONE OR !MOSTLY! DONE ^^ ----

ViewFactory: model_or_modelargs odd (simplify, streamline, more "data-driven"?!)
  create new standard type by args:  view.text(text=foo, style="secondary")
  same but with some subclass of the standard type:  view.text(Foo, text=foo, style="secondary") 
                                                     or view.text(Foo(text=foo, style="secondary"))
  existing model:  view.text.for_model(my_model)
  with some view_hints:
    view.text(text=foo, style="secondary", view_hints=dict(...))
    view.text(Foo, text=foo, style="secondary", view_hints=dict(...)) 
    view.text.for_model(my_model, view_hints=dict(...))
driver specific properties, either in View or specifically in some subclass, tooltips/...
  __call__(self, model_or_modeltype, /, *, view_hints=None, **kwargs)


app model: window title, title2, actions, icon, body view, closing:bool, applicationname (gtk)

observable: have a cookie to detect if source observables are unchanged or needs re-computation

observable lists (additional events: item added, item removed)
  
------- ^^ IN CONSTRUCTION ^^ -------

model needs to know host?
  threading? -> assume(assert?) that we are always in the right thread for actions and .map - use threadpool for stuff
  reactivity dependencies detection?
view needs to know host?
  threading?
  reactivity dependencies detection?

drivers: to what drivers an app is compatible with?
nicer ide support for stuff like observables
selection models (single, multi); knows the orig list, removes items once the origin was removed
computed observables in models (we only have code for that in views) -> same but with 'self'
async computedobsvls (mostly: allow to specify what value it has during computation)
mainloop, async -> specify good interface or protocol
threading (always main?) - how to keep ui thread mostly idle?
toast notifications; by action context.toastfoo() (also overlays? -> no)
pieces.interact
  file/dir chooser dialog
i18n for klovve's own strings: gettext based, but changeable in app creation
action context.dialog(); always modal
  kind: INLINE|EXTERNAL (gtk: popover/dialog)
  title (ignored e.g. for INLINE)
  closable: True
views: visible, activated; in Model (derived from BareModel); or as adapter widgets?!
2nd level tabs (Gtk.Stack based)
gtk: some nice (static?!) animations
named (list_)observables; with file storage?! (for application settings)
gtk: remove widget from last parent before adding to something
error handling: try/except whenever custom code runs; "app crashed. [more]"~>callstack, continue
event defer&cut_off
icons (by freedesktop name & textual symbol) / images (bytes + mimetype)
action loading animations; with context.busyfoo(text=None,kind=INLINE):...
menu buttons: model.triggers is list of button|triggergroup(separators); make triggers checkable
label mnemonic accelerators (optionally via some 'mnemonic' flag; then like in gtk or similar)
listview: optional searching box
labels, texts: some (semantic) styling
radiobtn/multilinetext/combobox/dropdownedittext/linkbutton/accordion/breadcrumb/toggles(btnbar)
  "close" action - default impl calls just ".stop()", others can make dialogs before and decide
responsive designs?
boxes: columns(h) / pile(v) ; all childs: align=fill ; expand (gtk: hexpand for columns; vexpand for pile - or both?!)
annizestudiolike (boxes inside boxes, with stuff inside)
consoleview (like annize do, or krrez runnerview)
in-app help (same as tooltips?)
"""
