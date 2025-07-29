#!/usr/bin/env python3

import os
import json
import subprocess

from PluginsPy.MainUI import *
from PluginsPy.Tools import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class CmdSets:

    def __init__(self, ui: Ui_MainWindow, MainWindow: QMainWindow):
        self.ui               = ui
        self.gridLayout       = ui.PSGridLayout
        self.MainWindow       = MainWindow

        self.configPath = 'CmdSets'
        self.loadConfig()

        ui.CSSelectByFileNameComboBox.currentIndexChanged.connect(self.SelectByFileNameChanged)
        ui.CSSelectByCmdsetComboBox.currentIndexChanged.connect(self.SelectByCmdsetChanged)

        self.ui.CSSelectByFileNameComboBox.addItems(self.fileNames)
        self.ui.CSRunAllPushButton.clicked.connect(self.cmdRunAllClicked)

    def loadConfig(self):
        self.cmdSets = []
        self.fileNames = getFiles(self.configPath)

        for f in self.fileNames:
            configFile = self.configPath + '/' + f
            if os.path.exists(configFile):
                with open(configFile, 'r') as f:
                    self.cmdSets.append(json.load(f))

        print(self.fileNames)
        print(self.cmdSets)

    def SelectByFileNameChanged(self):
        print("SelectByFileNameChanged")

        self.fileIndex = self.ui.CSSelectByFileNameComboBox.currentIndex()
        self.cmdsets = [cmdset["name"] for cmdset in  self.cmdSets[self.fileIndex]["cmdsets"]]
        self.ui.CSSelectByCmdsetComboBox.clear()
        self.ui.CSSelectByCmdsetComboBox.addItems(self.cmdsets)

    def SelectByCmdsetChanged(self):
        print("SelectByCmdsetChanged")

        self.cmdsetIndex = self.ui.CSSelectByCmdsetComboBox.currentIndex()
        self.cmdset = self.cmdSets[self.fileIndex]["cmdsets"][self.cmdsetIndex]
        self.fillPSGridLayout(self.ui.CSCmdsGridLayout, self.cmdset["cmds"])

    def fillPSGridLayout(self, gridLayout: QGridLayout, cmds: list):
        i = 0

        # clear
        item_list = list(range(gridLayout.count()))
        item_list.reverse()# 倒序删除，避免影响布局顺序

        for i in item_list:
            item = gridLayout.itemAt(i)
            gridLayout.removeItem(item)
            if item.widget():
                item.widget().deleteLater()

        for cmd in cmds:
            label = QLabel(cmd["name"])
            value = QLineEdit(cmd["cmd"])
            gridLayout.addWidget(label, i, 0, 1, 1)
            gridLayout.addWidget(value, i, 1, 1, 1)

            button = QPushButton("run")
            button.clicked.connect(self.cmdRunClicked)
            gridLayout.addWidget(button, i, 2, 1, 1)

            i += 1

    def findWidgetPosition(self, gridLayout):
        print("row, col: " + str(gridLayout.rowCount()) + ", " + str(gridLayout.columnCount()))
        for i in range(gridLayout.rowCount()):
            for j in range(gridLayout.columnCount()):
                if gridLayout.itemAtPosition(i, j) != None and (gridLayout.itemAtPosition(i, j).widget() == self.MainWindow.sender()):
                    return (i, j)

        return (-1, -1)

    def cmdRunClicked(self):
        print("cmdRunClicked")
        row, col = self.findWidgetPosition(self.ui.CSCmdsGridLayout)
        cmd: str = self.cmdset["cmds"][row]["cmd"]
        print("cmd: " + cmd)

        out = subprocess.Popen(cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out.wait()
        data = out.stdout.read()
        print(data.decode('utf-8').strip())

    def cmdRunAllClicked(self):
        print("cmdRunAllClicked")
        for row in range(len(self.cmdset["cmds"])):
            cmd: str = self.cmdset["cmds"][row]["cmd"]
            print("cmd: " + cmd)

            out = subprocess.Popen(cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            out.wait()
            data = out.stdout.read()
            print(data.decode('utf-8').strip())

            if out.returncode != 0:
                break
