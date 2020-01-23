# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from maya import cmds
from maya import mel


def onMayaDroppedPythonFile(*args, **kwargs):
    """for Maya2017.3+"""
    _register_hotkey()


def onMayaDroppedMelFile():
    "for old Maya"
    _register_hotkey()


def _register_hotkey():
    script_path = os.path.dirname(__file__) + "/scripts"

    command = """
# -------------------------
# MayaWindowSwitcher
# Author: @tm8r
# https://github.com/tm8r/MayaWindowSwitcher
# -------------------------

import os
import sys

from maya import cmds

def switch_window():
    script_path = "{0}"
    if not os.path.exists(script_path):
        cmds.error("WindowSwitcher install directory is not found. path={0}")
        return
    if script_path not in sys.path:
        sys.path.insert(0, script_path)

    import window_switcher.view
    window_switcher.view.WindowSwitcher.switch()

switch_window()""".format(script_path)

    command_name = "WindowSwitcher"
    if cmds.runTimeCommand(command_name, ex=True):
        cmds.runTimeCommand(command_name, e=True, delete=True)
    cmds.runTimeCommand(
        command_name,
        ann="Open WindowSwitcher",
        category="User",
        command=command,
        commandLanguage="python"
    )
    named_command = command_name + "Command"
    named_command = cmds.nameCommand(
        named_command,
        annotation="Open WindowSwitcher",
        command=command_name,
    )
    if int(cmds.about(v=True)) <= 2015:
        cmds.hotkey(k="T", ctl=True, n=named_command)
        return

    cmds.hotkey(k="t", ctl=True, sht=True, n=named_command)


if __name__ == "_installHotkeyTm8rWindowSwitcher":
    onMayaDroppedMelFile()
