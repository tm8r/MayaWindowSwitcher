# -*- coding: utf-8 -*-
u"""Layout library"""
from __future__ import absolute_import, division, print_function


def clear_layout(layout):
    u"""clear layout

    Args:
        layout (Qt.QtWidgets.QBoxLayout): target layout
    """
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            else:
                clear_layout(item.layout())
