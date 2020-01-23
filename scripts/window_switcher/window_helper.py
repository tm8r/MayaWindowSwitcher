# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from window_switcher.vendor.Qt import QtWidgets

_MAYA_MAIN_WINDOW_NAME = "MayaWindow"


def collect_switchable_windows(parent=None):
    switchable_windows = []
    for w in QtWidgets.QApplication.topLevelWidgets():
        if not w.isVisible():
            continue
        if w.objectName() == _MAYA_MAIN_WINDOW_NAME:
            continue
        if parent and w == parent:
            continue
        if not w.children():
            continue
        if w.isActiveWindow():
            continue

        if not w.windowTitle() and w.height() < 20:
            # workaround for Maya2019 outliner bug.
            continue

        switchable_windows.append(w)
    return switchable_windows
