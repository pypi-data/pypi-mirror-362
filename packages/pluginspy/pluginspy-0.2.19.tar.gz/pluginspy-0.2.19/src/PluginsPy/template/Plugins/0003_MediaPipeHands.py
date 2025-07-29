#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: FolderLevel
Date: 2024-09-29 09:02:56
License: MIT License
"""

import datetime

from PluginsPy.VisualLogPlot import VisualLogPlot

import matplotlib.pyplot as plot
from matplotlib.figure import Figure
from matplotlib.axes import Axes

class MediaPipeHands:

    """
    @data(input/0003_hands.txt): None
    """

    def __init__(self, kwargs):

        print("MediaPipeHands args:")
        print(kwargs)

        data = kwargs["data"]

        parseFilenames = [data]
        regex = [
            'x\s*=\s*([-]?\d.\d+),\s*y\s*=\s*([-]?\d.\d+),\s*z\s*=\s*([-]?\d.\d+)'
            ]
        kwargs["filesLineInfos"], filenames = VisualLogPlot.parseData(
                parseFilenames,
                regex,
            )

        plotType             = "3D"
        kwargs["xAxis"]      = [0]
        kwargs["dataIndex"]  = [0, 1, 2]
        kwargs["plotType"]   = "3D"

        VisualLogPlot.show(kwargs)
