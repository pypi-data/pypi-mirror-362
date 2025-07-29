#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: zengjf
Date: 2024-10-01 11:15:38
License: MIT License
"""

import datetime

from PluginsPy.VisualLogPlot import VisualLogPlot

import matplotlib.pyplot as plot
from matplotlib.figure import Figure
from matplotlib.axes import Axes

class KernelKeyDiff:

    """
    @first(input/0005_kernel_1_keydiff.txt): None
    @second(input/0005_kernel_2_keydiff.txt): None
    """

    def __init__(self, kwargs):

        print("KernelKeyDiff args:")
        print(kwargs)

        first = kwargs["first"]
        second = kwargs["second"]

        parseFilenames = [first, second]
        regex = [
            '(\d*\.\d*)\s+:.*(Kernel_init_done)',
            '(\d*\.\d*)\s+:.*(INIT:late-init)',
            '(\d*\.\d*)\s+:.*(vold:fbeEnable:START)',
            '(\d*\.\d*)\s+:.*(INIT:post-fs-data)'
            ]
        kwargs["filesLineInfos"], filenames = VisualLogPlot.parseData(
            parseFilenames,
            regex,
            )

        kwargs["plotType"]   = "keyDiff"
        kwargs["xAxis"]      = [1]
        kwargs["dataIndex"]  = [0]

        VisualLogPlot.show(kwargs)
