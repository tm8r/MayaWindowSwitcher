# -*- coding: utf-8 -*-
"""manage style sheet"""
from __future__ import absolute_import, division, print_function

import os

_RESOURCES_DIRECTORY = os.path.join(os.path.dirname(__file__), "resources")


class StyleSheet(object):
    """manage style sheet"""

    _CSS_DICT = {}

    def __init__(self):
        """initialize"""
        self._core_css = _read_text(_RESOURCES_DIRECTORY + "/core.css")

    @property
    def core_css(self):
        """get core css

        Returns:
            str: core css
        """
        return self._core_css

    def get_css(self, path):
        """get merged css(core css and unique css)

        Args:
            path (str): css path

        Returns:
            unicode: result css
        """
        if path not in self._CSS_DICT:
            self._CSS_DICT[path] = _read_text(path)
        return self._core_css + self._CSS_DICT[path]

    def reload(self):
        """reload CSS(for develop)"""
        self._core_css = _read_text(_RESOURCES_DIRECTORY + "/core.css")
        self._CSS_DICT = {}


def _read_text(path):
    res = ""
    if not os.path.isfile(path):
        return res
    with open(path, "r") as f:
        res = f.read()
    return res
