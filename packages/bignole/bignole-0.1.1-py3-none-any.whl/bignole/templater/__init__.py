# -*- coding: utf-8 -*-


import os

from importlib import import_module
from pkgutil import iter_modules

from .dummy import Templater


DEFAULT_RESOLVE_SEQ = "mako", "jinja"
TEMPLATER_NAMES = {
    "dummy": "Templater",
    "mako": "MakoTemplater",
    "jinja": "JinjaTemplater",
}


def all_templaters():
    """Get all available templaters"""
    templaters = {}

    pkgname = __package__
    pkgpath = os.path.dirname(__file__)
    for module_info in iter_modules(path=[pkgpath], prefix=f"{pkgname}."):
        try:
            name = module_info.name
            sname = name.split(".")[-1]
            templaters[sname] = getattr(import_module(name), TEMPLATER_NAMES[sname])
        except:  # pylint: disable-msg=bare-except
            pass

    return templaters


def resolve_templater(choose=None, order=DEFAULT_RESOLVE_SEQ):
    """Return templater if available"""
    templaters = all_templaters()
    found = None

    if choose and choose in templaters:
        found = templaters[choose]
    else:
        for code in order:
            if code in templaters:
                found = templaters[code]
                break
        else:
            found = Templater

    return found()
