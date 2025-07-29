#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: zengjf
Date: 2024-10-01 11:17:22
License: MIT License
"""

import datetime

from PluginsPy.VisualLogPlot import VisualLogPlot

import matplotlib.pyplot as plot
from matplotlib.figure import Figure
from matplotlib.axes import Axes

class KernelKey:

    """
    @first(input/0004_kernel_1.txt): None
    @second(input/0004_kernel_2.txt): None
    """

    def __init__(self, kwargs):

        print("Kernel args:")
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

        kwargs["plotType"]   = "key"
        kwargs["xAxis"]      = [1]
        kwargs["dataIndex"]  = [0]

        VisualLogPlot.show(kwargs)
