# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os
from window_switcher.vendor.Qt import QtCompat
from window_switcher.vendor.Qt import QtCore
from window_switcher.vendor.Qt import QtGui
from window_switcher.vendor.Qt import QtWidgets

from window_switcher.libs.qt.layout import clear_layout
from window_switcher.libs.qt.stylesheet import StyleSheet
from window_switcher import settings
from window_switcher import window_helper

from maya import OpenMayaUI as omui

try:
    MAYA_WINDOW = QtCompat.wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
except:
    MAYA_WINDOW = None

_RESOURCES_DIRECTORY = os.path.join(os.path.dirname(__file__), "resources")

_NO_IMAGE_PIXMAP = QtGui.QPixmap(_RESOURCES_DIRECTORY + "/no_image.png")

_WINDOW_HORIZONTAL_SIZE = 4

_WINDOW_ELEMENT_WIDTH = 160
_WINDOW_BUTTON_HEIGHT = 140


class WindowSwitcher(QtWidgets.QDialog):
    _INSTANCE = None  # type: WindowSwitcher
    _ACTIVE = False

    def __init__(self, parent=MAYA_WINDOW):
        u"""initialize"""
        super(WindowSwitcher, self).__init__(parent=parent)
        self._windows = []
        self._buttons = []
        self._current_index = 0

        self.setWindowTitle("WindowSwitcher")
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.setObjectName("WindowSwitcher")
        self.setStyleSheet(StyleSheet().get_css(_RESOURCES_DIRECTORY + "/window_switcher.css"))

        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.setMinimumSize(QtCore.QSize(480, 200))

        root_layout = QtWidgets.QGridLayout()
        root_layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(root_layout)

        self.main_layout = QtWidgets.QVBoxLayout()
        root_layout.addLayout(self.main_layout, 0, 0, 1, 1)

        self._refresh()

    @classmethod
    def open(cls, *args):
        u"""UIを表示"""
        win = cls._INSTANCE
        if not win:
            win = cls()
            cls._INSTANCE = win
        cls._ACTIVE = True
        win.show()
        win.activateWindow()

    @classmethod
    def switch(cls):
        if cls._INSTANCE and cls._ACTIVE:
            win = cls._INSTANCE
            win._switch_selection()
            return
        if cls._INSTANCE and not cls._ACTIVE:
            cls._ACTIVE = True
            win = cls._INSTANCE
            win._refresh()
            win.show()
            win.activateWindow()
            return
        cls.open()

    def _change_index(self, index):
        self._current_index = index
        self.close()

    def _refresh(self):
        clear_layout(self.main_layout)
        self._current_index = 0
        self._buttons = []
        self._windows = window_helper.collect_switchable_windows(self)
        if not self._windows:
            warn_label = QtWidgets.QLabel("No switchable windows.")
            warn_label.setAlignment(QtCore.Qt.AlignCenter)
            self.main_layout.addWidget(warn_label)
            return
        layout = None
        for index, w in enumerate(self._windows):
            if index == 0 or index % _WINDOW_HORIZONTAL_SIZE == 0:
                layout = QtWidgets.QHBoxLayout()
                self.main_layout.addLayout(layout)
            icon_layout = QtWidgets.QVBoxLayout()
            layout.addLayout(icon_layout)
            button = QtWidgets.QToolButton()
            button.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            button.customContextMenuRequested.connect(
                lambda x, y=button, z=w: self._on_window_button_context_menu_requested(x, y, z))
            button.setIconSize(QtCore.QSize(_WINDOW_ELEMENT_WIDTH, _WINDOW_BUTTON_HEIGHT))
            icon = QtGui.QIcon()

            if settings.is_simple_mode():
                icon.addPixmap(_NO_IMAGE_PIXMAP)
            else:
                win_pix = QtGui.QPixmap.grabWindow(w.winId())
                icon.addPixmap(win_pix, QtGui.QIcon.Normal,
                               QtGui.QIcon.Off)

            button.setIcon(icon)
            button.setCheckable(True)
            button.setFixedWidth(_WINDOW_ELEMENT_WIDTH)
            button.setFixedHeight(_WINDOW_BUTTON_HEIGHT)
            button.clicked.connect(lambda x=index: self._change_index(x))
            icon_layout.addWidget(button)
            label = QtWidgets.QLabel(w.windowTitle())
            label.setMaximumWidth(_WINDOW_ELEMENT_WIDTH)
            label.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
            icon_layout.addWidget(label)
            self._buttons.append(button)

        self._buttons[0].setChecked(True)

    def _on_window_button_context_menu_requested(self, point, button, window):
        menu = QtWidgets.QMenu(button)
        move_action = QtWidgets.QAction("Reset Position", button)
        main_window_center = MAYA_WINDOW.rect().center()
        left = main_window_center.x() - window.width() / 2
        top = main_window_center.y() - window.height() / 2

        move_action.triggered.connect(lambda x=window, y=left, z=top: x.move(y, z))
        menu.addAction(move_action)
        menu.exec_(button.mapToGlobal(point))

    def _switch_selection(self):
        self._current_index += 1
        if self._current_index >= len(self._windows):
            self._current_index = 0
        for index, b in enumerate(self._buttons):
            if index == self._current_index:
                b.setChecked(True)
                continue
            b.setChecked(False)

    # region event override
    # override
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), QtGui.QColor(0, 0, 0, 150))

    # override
    def keyReleaseEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            # prevent reject
            return
        if event.modifiers() != QtCore.Qt.NoModifier:
            event.accept()
            return
        self.close()

    # override
    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.ActivationChange and not self.isActiveWindow() and self.isVisible():
            self.close()
            return
        super(WindowSwitcher, self).changeEvent(event)

    # override
    def closeEvent(self, event):
        super(WindowSwitcher, self).closeEvent(event)
        WindowSwitcher._ACTIVE = False
        if not self._windows:
            return
        window = self._windows[self._current_index]
        if window.isMinimized():
            window.setWindowState(window.windowState() & ~QtCore.Qt.WindowMinimized)
        window.activateWindow()

    # endregion event override
