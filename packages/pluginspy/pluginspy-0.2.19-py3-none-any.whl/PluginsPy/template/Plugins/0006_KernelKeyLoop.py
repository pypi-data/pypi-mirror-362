#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: zengjf
Date: 2024-10-01 11:14:47
License: MIT License
"""

import datetime

from PluginsPy.VisualLogPlot import VisualLogPlot

import matplotlib.pyplot as plot
from matplotlib.figure import Figure
from matplotlib.axes import Axes

class KernelKeyLoop:

    """
    @first(input/0004_kernel_1.txt): None
    """

    def __init__(self, kwargs):

        print("KernelKeyLoop args:")
        print(kwargs)

        first = kwargs["first"]

        parseFilenames = [first]
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

        kwargs["plotType"]   = "keyLoop"
        kwargs["xAxis"]      = [1]
        kwargs["dataIndex"]  = [0]

        VisualLogPlot.show(kwargs)
