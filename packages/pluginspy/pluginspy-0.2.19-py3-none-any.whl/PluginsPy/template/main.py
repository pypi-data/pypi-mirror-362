#!/usr/bin/env python3

import PluginsPy
import os
import sys

if __name__ == "__main__" :
    if (len(sys.argv) == 2 and sys.argv[1] == "qt"):
        PluginsPy.PluginsPyQT5()
    else:
        sys.path.append(os.path.dirname(__file__))
        # PluginsPy.PluginsPy(__file__)
        PluginsPy.PluginsPySelect(__file__)
