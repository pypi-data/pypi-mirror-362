#!/usr/bin/env python3

import os
import json

class Config:
    Version = "0.0.1"
    PlotType = ["normal", "key", "keyLoop", "keyDiff", "3D"]

    def __init__(self):
        self.configPath = 'output/PluginsPyConfig.txt'
        self.keyValues = self.loadConfig()

        if "version" not in self.keyValues.keys() or self.keyValues["version"] != Config.Version:
            self.keyValues = {"version": Config.Version}

        if "regexTemplate" not in self.keyValues.keys():
            defaultRegexTemplat = []
            defaultRegexTemplat.append({
                "name": "current",
                "regex": "(\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\.\d*)\s+\d+\s+\d+\s+\w+\s+.*: in wakeup_callback: resumed from suspend (\d+)",
                "xAxis": [0],
                "dataIndex": [0, 1],
                "plotType": "normal"
                })
            defaultRegexTemplat.append({
                "name": "logcat",
                "regex": "(\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\.\d*)\s+\d+\s+\d+\s+\w+\s+.*: in wakeup_callback: resumed from suspend (\d+)",
                "xAxis": [0],
                "dataIndex": [0, 1],
                "plotType": "normal"
                })
            defaultRegexTemplat.append({
                "name": "key",
                "regex": "(\d*\.\d*)\s+:.*(Kernel_init_done)\n(\d*\.\d*)\s+:.*(INIT:late-init)\n(\d*\.\d*)\s+:.*(vold:fbeEnable:START)\n(\d*\.\d*)\s+:.*(INIT:post-fs-data)",
                "xAxis": [1],
                "dataIndex": [0],
                "plotType": "key"
                })
            defaultRegexTemplat.append({
                "name": "keyLoop",
                "regex": "(\d*\.\d*)\s+:.*(Kernel_init_done)\n(\d*\.\d*)\s+:.*(INIT:late-init)\n(\d*\.\d*)\s+:.*(vold:fbeEnable:START)\n(\d*\.\d*)\s+:.*(INIT:post-fs-data)",
                "xAxis": [1],
                "dataIndex": [0],
                "plotType": "keyLoop"
                })
            defaultRegexTemplat.append({
                "name": "keyDiff",
                "regex": "(\d*\.\d*)\s+:.*(Kernel_init_done)\n(\d*\.\d*)\s+:.*(INIT:late-init)\n(\d*\.\d*)\s+:.*(vold:fbeEnable:START)\n(\d*\.\d*)\s+:.*(INIT:post-fs-data)",
                "xAxis": [1],
                "dataIndex": [0],
                "plotType": "keyDiff"
                })
            defaultRegexTemplat.append({
                "name": "3D",
                "regex": "x\s*=\s*([-]?\d.\d+),\s*y\s*=\s*([-]?\d.\d+),\s*z\s*=\s*([-]?\d.\d+)",
                "xAxis": [0],
                "dataIndex": [0, 1, 2],
                "plotType": "3D"
                })

            self.keyValues["regexTemplate"] = defaultRegexTemplat

        self.saveConfig()

    def loadConfig(self):
        if not os.path.exists("output"):
            os.mkdir("output")

        if os.path.exists(self.configPath):
            with open(self.configPath, 'r') as f:
                return json.load(f)
        else:
            return {}
    
    def saveConfig(self):
        if not os.path.exists("output"):
            os.mkdir("output")

        jsonStr = json.dumps(self.keyValues, indent=4)
        with open(self.configPath, 'w') as f:
            f.write(jsonStr)
 
    def setKeyValue(self, key, value):
        self.keyValues[key] = value

    def getValue(self, key):
        if key in self.keyValues.keys():
            return self.keyValues[key]
        else:
            return None

    def setKeyValues(self, keyValues: dict):
        saveConfig = dict(keyValues)
        for key in saveConfig:
            self.keyValues[key] = saveConfig[key]

    def replaceKeyValues(self, target: dict, src: dict):
        for key in src.keys():
            target[key] = src[key]
 