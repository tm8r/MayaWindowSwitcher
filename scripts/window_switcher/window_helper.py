# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from window_switcher.vendor.Qt import QtWidgets

_MAYA_MAIN_WINDOW_NAME = "MayaWindow"


def collect_switchable_windows(parent=None):
    switchable_windows = []
    active_window = None
    for w in QtWidgets.QApplication.topLevelWidgets():
        if not w.isVisible():
            continue
        if parent and w == parent:
            continue
        if not w.children():
            continue
        if w.isActiveWindow():
            active_window = w
            continue

        if not w.windowTitle() and w.height() < 20:
            # workaround for Maya2019 outliner bug.
            continue

        switchable_windows.append(w)

    if active_window:
        switchable_windows.insert(0, active_window)
    return switchable_windows
