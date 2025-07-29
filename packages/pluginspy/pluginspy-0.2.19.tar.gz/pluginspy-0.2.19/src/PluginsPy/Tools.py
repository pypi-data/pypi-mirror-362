#!/usr/bin/env python3

import os

def getFiles(path) :
    for (dirpath, dirnames, filenames) in os.walk(path) :
        dirpath = dirpath
        dirnames = dirnames
        filenames = filenames

        return filenames

    return []
