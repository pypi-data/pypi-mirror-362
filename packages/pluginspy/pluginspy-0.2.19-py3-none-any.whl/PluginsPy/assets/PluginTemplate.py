#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: ${author}
Date: ${date}
License: MIT License
"""

import datetime

from PluginsPy.VisualLogPlot import VisualLogPlot

import matplotlib.pyplot as plot
from matplotlib.figure import Figure
from matplotlib.axes import Axes

class ${className}:

    """
    ${defaultArgs}
    """

    def __init__(self, kwargs):

        print("${className} args:")
        print(kwargs)

        ${instanceArgs}

        parseFilenames = [${parseFilenames}]
        regex = [${regex}]
        kwargs["filesLineInfos"], filenames = VisualLogPlot.parseData(
            parseFilenames,
            regex,
            )

        kwargs["plotType"]  = "${plotType}"
        kwargs["xAxis"]      = [${xAxis}]
        kwargs["dataIndex"]  = [${dataIndex}]

        VisualLogPlot.show(kwargs)
