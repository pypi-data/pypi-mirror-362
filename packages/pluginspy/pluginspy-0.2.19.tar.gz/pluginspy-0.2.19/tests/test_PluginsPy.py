# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

import unittest

from PluginsPy import PluginsPy

if __name__ == '__main__':
    # PluginsPy(__file__, skipedPlugins=["PluginExample"], pluginsDir="Plugins")
    PluginsPy(__file__, pluginsDir="Plugins")
