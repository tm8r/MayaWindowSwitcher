# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from maya import cmds

_SIMPLE_MODE_KEY = "window_switcher_simple_mode"
_SIMPLE_MODE_ENABLED = 1
_SIMPLE_MODE_DISABLED = 0


def is_simple_mode():
    return cmds.optionVar(q=_SIMPLE_MODE_KEY) == _SIMPLE_MODE_ENABLED


def enable_simple_mode():
    cmds.optionVar(iv=(_SIMPLE_MODE_KEY, _SIMPLE_MODE_ENABLED))


def disable_simple_mode():
    cmds.optionVar(iv=(_SIMPLE_MODE_KEY, _SIMPLE_MODE_DISABLED))
