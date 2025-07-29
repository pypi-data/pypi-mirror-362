#!/usr/bin/env python3

import importlib
import re
import os
import sys
import inspect
import subprocess

from PluginsPy.MainUI import *
from PluginsPy.Config import Config
from PluginsPy.PluginProcess import *
from PluginsPy.PluginTemplate import PluginTemplate

import VisualLog.LogParser as LogParser

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Plugin:

    def __init__(self, ui: Ui_MainWindow, MainWindow: QMainWindow):
        self.ui               = ui
        self.gridLayout       = ui.PSGridLayout
        self.MainWindow       = MainWindow
        self.config           = Config()
        self.currentThread: QThread = None

        # Plugins
        ui.PSPluginsComboBox.currentIndexChanged.connect(self.PSPluginsChanged)
        ui.PSPluginsComboBox.setStyleSheet("QComboBox{combobox-popup:0;}")
        ui.PSRunPushButton.clicked.connect(self.PSRunClick)
        ui.PSParseDataPushButton.clicked.connect(self.PSParseDataClick)
        ui.PSVisualLogPushButton.clicked.connect(self.PSVisualLogClick)
        ui.PSTempPushButton.clicked.connect(self.PSTempClick)
        ui.PSPlotTypeComboBox.addItems(Config.PlotType)
        ui.PSPlotTypeComboBox.setCurrentIndex(0)
        ui.PSSavePlotArgsPushButton.clicked.connect(self.PSSavePlotArgsClick)
        ui.PSRegexAddPushButton.clicked.connect(self.PSRegexAddClick)
        ui.PSRegexDelPushButton.clicked.connect(self.PSRegexDeleteClick)

        self.initPlugins()

        self.lineInfosOfFiles = []

        self.MainWindow.closeEvent = self.closeCallback

    def closeCallback(self, event):
        print("closeCallback")

        self.config.saveConfig()

    def getPluginsIndex(self, pluginsDir="Plugins") :

        filenames = []
        for file in os.listdir(pluginsDir):
            full_path = os.path.join(pluginsDir, file)
            if os.path.isfile(full_path):
                filenames.append(file)

        fileIndex = 0
        for file in filenames:
            if file == "__init__.py":
                continue

            moduleString = file.split(".")[0]
            matchObj = re.match(r'\d{4}[_]?', moduleString)
            if matchObj:
                currentIndex = int(matchObj.group(0).replace("_", ""))
                if currentIndex > fileIndex:
                    fileIndex = currentIndex

        print("current file index: " + str(fileIndex))

        return fileIndex

    def getVisualLogData(self):
        data = {}

        data["xAxis"]     = eval("[" + self.ui.PSXAxisLineEdit.text() + "]")
        data["dataIndex"] = eval("[" + self.ui.PSDataIndexLineEdit.text() + "]")
        data["plotType"]  = self.ui.PSPlotTypeComboBox.currentText()

        for i in range(len(data["xAxis"])):
            if data["xAxis"][i] < 0:
                data["xAxis"][i] = 0

        if len(data["dataIndex"]) == 0:
            data["dataIndex"].append(0)

        return data

    def PSVisualLogClick(self):

        '''
        利用反射处理绘图才不会导致当前UI异常
        '''

        print("PSVisualLogClick")

        self.visualLogData = self.getVisualLogData()

        try:
            moduleString = "VisualLogPlot"
            args = self.visualLogData
            args["filesLineInfos"] = self.lineInfosOfFiles

            if self.currentThread != None and self.currentThread.isRunning():
                print("please close current matplotlib ui")
            else:
                # Ubuntu下开进程绘图不显示
                if sys.platform.startswith("linux"):
                    self.ui.PSInfoPlainTextEdit.setPlainText(getClazzWithRun(moduleString, None, args))
                else:
                    self.currentThread = PluginProcess(moduleString, args, self.processRetData)
                    self.currentThread.start()
                    self.currentThread.finished.connect(self.updateInfo)
        except Exception as e:
            print(e)

    def PSParseDataClick(self):
        print("PSParseDataClick")

        self.lineInfosOfFiles = []

        regexArray = self.ui.PSRegexPlainTextEdit.toPlainText().strip().splitlines()
        print(regexArray)

        if len(regexArray) > 0:
            keyValues = self.getPluginKeyValues()

            # 整体调一次解析
            parseFiles = []
            for key in keyValues.keys():
                if "\\" in keyValues[key] or "/" in keyValues[key]:
                    print(key + " -> " + keyValues[key])

                    if os.path.exists(keyValues[key]):
                        print(keyValues[key])
                        # r"(\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\.\d*)\s+\d+\s+\d+\s+\w+\s+.*: In wakeup_callback: resumed from suspend"
                        parseFiles.append(keyValues[key])

                    else:
                        print("can't file path:" + keyValues[key])
            print(parseFiles)

            try:
                self.lineInfosOfFiles, filenames = LogParser.logFileParser(parseFiles, regexArray)
            except Exception as e:
                print(e)

        self.ui.PSInfoPlainTextEdit.setPlainText("")
        for lineInfos in self.lineInfosOfFiles:
            print("file data: ")
            for info in lineInfos:
                print(info)
                self.ui.PSInfoPlainTextEdit.appendPlainText(", ".join(str(v) for v in info))

    def PSRegexAddClick(self):
        print("PSRegexAddClick")
        name, ok=QInputDialog.getText(self.MainWindow, 'Text Input Dialog', 'regex name:', QLineEdit.Normal)

        if name in ["current", "logcat", "kernel"]:
            print("skip " + name)
            return

        if ok:
            regexTemplate = self.config.getValue("regexTemplate")
            modify = False

            for item in regexTemplate:
                if item["name"] == name:
                    self.config.replaceKeyValues(item, self.getCurrentTemplateConfigData())

                    modify = True

            if not modify:
                t = self.getCurrentTemplateConfigData()
                t["name"] = name

                regexTemplate.append(t)

            self.config.saveConfig()

            self.ui.PSRegexTemplateComboBox.currentIndexChanged.disconnect()
            self.ui.PSRegexTemplateComboBox.clear()
            self.ui.PSRegexTemplateComboBox.addItems([item["name"] for item in regexTemplate])
            self.ui.PSRegexTemplateComboBox.currentIndexChanged.connect(self.PSRegexTemplateChanged)

    def PSRegexDeleteClick(self):
        print("PSRegexDeleteClick")
        ret = QMessageBox.warning(self.MainWindow, "warning", "checkk to delete", QMessageBox.Yes | QMessageBox.No)
        if ret == QMessageBox.Yes:
            name = self.ui.PSRegexTemplateComboBox.currentText()

            if name in ["current", "logcat", "kernel"]:
                print("skip " + name)
                return

            regexTemplate: list = self.config.getValue("regexTemplate")
            deleteItem = None

            for item in regexTemplate:
                if item["name"] == name:
                    deleteItem = item

            if deleteItem != None:
                regexTemplate.remove(deleteItem)

            self.config.saveConfig()

            self.ui.PSRegexTemplateComboBox.currentIndexChanged.disconnect()
            self.ui.PSRegexTemplateComboBox.clear()
            self.ui.PSRegexTemplateComboBox.addItems([item["name"] for item in regexTemplate])
            self.ui.PSRegexTemplateComboBox.currentIndexChanged.connect(self.PSRegexTemplateChanged)

    def getCurrentTemplateConfigData(self):
        t = self.getVisualLogData()
        t["regex"] = self.ui.PSRegexPlainTextEdit.toPlainText().strip()

        return t

    def PSSavePlotArgsClick(self):
        print("PSSavePlotArgsClick")

        if not os.path.exists("output"):
            print("can't find output dir, skip save config")
            return

        # if "regexTemplate" not in configData.keys():
        if self.config.getValue("regexTemplate") != None:
            for t in self.config.getValue("regexTemplate"):
                if t["name"] == "current":
                    self.config.replaceKeyValues(t, self.getCurrentTemplateConfigData())

        self.config.saveConfig()

    def PSTempClick(self):
        print("PSTempClick")

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filePath, _ = QFileDialog.getSaveFileName(None,
                                              "Save File",
                                              os.getcwd() + "/Plugins",
                                              "All Files (*);;Text Files (*.txt)",
                                              options=options)
        if filePath.strip() == "":
            print("please input file name")
            return

        # Windows，os.getcwd path with "\"，QFileDialog get path with "/"
        relFilePath = filePath.replace(os.getcwd().replace("\\", "/"), "").replace("\\", "/")[1:]
        relFileDir = os.path.dirname(relFilePath)
        fileName = os.path.basename(relFilePath)
        fileName = fileName[0].upper() + fileName[1:]
        if not fileName.endswith(".py"):
            fileName += ".py"

        print(relFileDir)
        print(fileName)

        regexArray = self.ui.PSRegexPlainTextEdit.toPlainText().strip().replace("'", "\\'").splitlines()
        visualLogData = self.getVisualLogData()
        plotType = self.ui.PSPlotTypeComboBox.currentText()

        res = subprocess.run(["git", "config", "user.name"], stdout=subprocess.PIPE)
        authorName = res.stdout.strip().decode()
        if len(authorName) == 0:
            authorName = os.getlogin()

        clazzName = fileName
        currentPluginIndex = self.getPluginsIndex() + 1
        matchObj = re.match(r'\d{4}[_]?', fileName)
        if matchObj:
            clazzName = fileName.replace(matchObj.group(0), "").replace(".py", "")
        else:
            clazzName = fileName.replace(".py", "")
            fileName = ("%04d" % currentPluginIndex) + "_" + fileName

        pluginDataInfo = {
            "author": authorName,
            "className": clazzName,
            "regex": regexArray,
            "plotType": plotType,
            "xAxis": visualLogData["xAxis"],
            "dataIndex": visualLogData["dataIndex"]
        }
        pt = PluginTemplate(pluginDataInfo)
        pt.setDefaultArgs(self.getPluginKeyValues())
        pt.composite()

        with open(relFileDir + "/" + fileName, mode="w", encoding="utf-8") as f:
            f.write(pt.parseTemplate())

        self.initPlugins()

    def initPlugins(self):
        self.plugins     = {}
        self.firstPlugin = ""

        for f in self.getPluginFiles("Plugins"):
            moduleFile   = f.split(".")[0]
            moduleString = moduleFile

            if moduleFile == "__init__":
                continue

            matchObj     = re.match(r'\d{4}[_]?', moduleFile)
            if matchObj:
                moduleString = moduleFile.replace(matchObj.group(0), "")

            self.plugins[moduleString] = moduleFile

            if self.firstPlugin == "":
                self.firstPlugin = moduleString
 
        self.pluginsKeys = list(self.plugins.keys())
        self.ui.PSPluginsComboBox.blockSignals(True)
        self.ui.PSPluginsComboBox.clear()
        self.ui.PSPluginsComboBox.addItems(self.plugins.values())
        self.ui.PSPluginsComboBox.blockSignals(False)

        self.setSavedConfig()

    def setSavedConfig(self):
        configData = self.config.keyValues

        if "pluginIndex" in configData.keys() and (configData["pluginIndex"] < len(self.plugins.values()) and configData["pluginIndex"] != 0):
            self.ui.PSPluginsComboBox.setCurrentIndex(configData["pluginIndex"])
        else:
            self.PSPluginsChanged()

        templateNames = [item["name"] for item in configData["regexTemplate"]]
        self.ui.PSRegexTemplateComboBox.addItems(templateNames)
        if self.config.getValue("selectRegexTemplate") in templateNames:
            self.ui.PSRegexTemplateComboBox.setCurrentText(self.config.getValue("selectRegexTemplate"))
        self.ui.PSRegexTemplateComboBox.currentIndexChanged.connect(self.PSRegexTemplateChanged)

        configData = None
        for t in self.config.getValue("regexTemplate"):
            # 没找到就用current，找到了就是当前配置中加载的
            if t["name"] == self.config.getValue("selectRegexTemplate"):
                configData = t
                break

            if t["name"] == "current":
                configData = t

        if configData != None:

            if "regex" in configData.keys():
                self.ui.PSRegexPlainTextEdit.setPlainText(configData["regex"])
            else:
                self.ui.PSRegexPlainTextEdit.setPlainText("(\\d{2}-\\d{2}\\s+\\d{2}:\\d{2}:\\d{2}\\.\\d*)\\s+\\d+\\s+\\d+\\s+\\w+\\s+.*: In wakeup_callback: resumed from suspend (\\d+)")

            if "xAxis" in configData.keys():
                self.ui.PSXAxisLineEdit.setText(",".join([str(i) for i in configData["xAxis"]]))
            else:
                self.ui.PSXAxisLineEdit.setText("0")

            if "dataIndex" in configData.keys():
                self.ui.PSDataIndexLineEdit.setText(",".join([str(i) for i in configData["dataIndex"]]))
            else:
                self.ui.PSDataIndexLineEdit.setText("0, 1")

            if "plotType" in configData.keys():
                self.ui.PSPlotTypeComboBox.setCurrentText(configData["plotType"])

    def fillPSGridLayout(self, gridLayout: QGridLayout, keyValues: dict):
        i = 0
        if len(keyValues) == 0:
            '''
            blank labels just to take up space
            '''
            label = QLabel("")
            value = QLabel("")
            gridLayout.addWidget(label, i, 0, 1, 1)
            gridLayout.addWidget(value, i, 1, 1, 1)
        else:
            for key in keyValues.keys():
                label = QLabel(key)
                if isinstance(keyValues[key], str):
                    value = QLineEdit(keyValues[key])
                    gridLayout.addWidget(label, i, 0, 1, 1)
                    gridLayout.addWidget(value, i, 1, 1, 1)

                    if "/" in keyValues[key] or "\\" in keyValues[key]:
                        button = QPushButton("Select File ...")
                        button.clicked.connect(self.PSPluginsArgsClicked)
                        gridLayout.addWidget(button, i, 2, 1, 1)
                else:
                    # {
                    #   'name': [
                    #     'zengaz',                 --> default value
                    #     ['zengjf', 'zengaz']      --> list value
                    #   ],
                    #   'id': '123456'
                    # }
                    #
                    # * key
                    # * value
                    #   * str
                    #     * default value
                    #   * list
                    #     * [0]: default value
                    #     * [1]: list value
                    value = QComboBox()
                    comboxValue = (list)(keyValues[key][1])
                    value.addItems(comboxValue)

                    gridLayout.addWidget(label, i, 0, 1, 1)
                    gridLayout.addWidget(value, i, 1, 1, 1)

                    value.currentIndexChanged.connect(self.PSArgsComboxChanged)
                    value.setCurrentIndex(comboxValue.index(keyValues[key][0]))

                i += 1

    def PSPluginsArgsClicked(self):
        print("PSPluginsClicked")
        row, col = self.findWidgetPosition(self.ui.PSGridLayout)

        if self.config.getValue("selectFileDir") == None or not os.path.exists(self.config.getValue("selectFileDir")):
            self.config.setKeyValue("selectFileDir", os.getcwd())
            self.config.saveConfig()

        fileNames, fileType = QFileDialog.getOpenFileNames(None, "select file", self.config.getValue("selectFileDir"), "All Files(*);;Text Files(*.txt)")
        if (len(fileNames) > 0):
            print(fileNames)
            print(fileType)

            edit: QLineEdit = self.ui.PSGridLayout.itemAtPosition(row, col - 1).widget()
            edit.setText(";".join(fileNames))

            self.config.setKeyValue("selectFileDir", os.path.dirname(fileNames[0]))

    def findWidgetPosition(self, gridLayout):
        print("row, col: " + str(gridLayout.rowCount()) + ", " + str(gridLayout.columnCount()))
        for i in range(gridLayout.rowCount()):
            for j in range(gridLayout.columnCount()):
                if gridLayout.itemAtPosition(i, j) != None and (gridLayout.itemAtPosition(i, j).widget() == self.MainWindow.sender()):
                    return (i, j)

        return (-1, -1)

    def getClazzArgs(self, moduleString):
        keyValues = {}

        try:
            # import file
            module   = importlib.import_module("Plugins." + self.plugins[moduleString])
            # get class
            clazz    = getattr(module, moduleString)
            # get class doc
            clazzDoc = clazz.__doc__

            # 从类注释中获取类参数及参数说明，格式@argument: argument doc
            if clazzDoc != None:
                for arg in clazzDoc.split("\n"):
                    keyValueSelect = []
                    keyValue = arg.strip().split(":")
                    if len(keyValue) == 2 and keyValue[0].strip().startswith("@"):
                        if "|" in keyValue[1]:
                            for item in keyValue[1].strip().split("|"):
                                if len(item.strip()) != 0:
                                    keyValueSelect.append(item.strip())

                        key = keyValue[0].strip().replace("@", "")
                        matchObj     = re.match(r'(.*)\((.*)\)', key)
                        if matchObj:
                            keyValue = matchObj.groups()

                            if len(keyValueSelect) != 0:
                                keyValues[keyValue[0]] = [keyValue[1], keyValueSelect]
                            else:
                                keyValues[keyValue[0]] = keyValue[1]
        except Exception as e:
            print(e)

        return keyValues

    def updateInfo(self):
        if (len(self.procRetData) > 0):
            self.ui.PSInfoPlainTextEdit.setPlainText(self.procRetData)

    def processRetData(self, data):
        self.procRetData = data

    def PSRunClick(self):
        print("PSRunClick")

        if self.currentThread != None and self.currentThread.isRunning():
            print("please close current matplotlib ui")
        else:
            keyValues = self.getPluginKeyValues()
            moduleString = self.plugins[self.pluginsKeys[self.ui.PSPluginsComboBox.currentIndex()]]
            # Ubuntu下开进程绘图不显示
            if sys.platform.startswith("linux"):
                self.ui.PSInfoPlainTextEdit.setPlainText(getClazzWithRun(moduleString, None, keyValues))
            else:
                self.currentThread = PluginProcess(moduleString, keyValues, self.processRetData)
                self.currentThread.start()
                self.currentThread.finished.connect(self.updateInfo)

    def getPluginKeyValues(self):
        keyValues = {}
        for i in range(self.ui.PSGridLayout.rowCount()):
            if self.ui.PSGridLayout.itemAtPosition(i, 0) == None:
                continue

            key = self.ui.PSGridLayout.itemAtPosition(i, 0).widget().text()
            # skip blank labels just to take up space
            if len(key) != 0:
                valueWidget = self.ui.PSGridLayout.itemAtPosition(i, 1).widget()
                if isinstance(valueWidget, QLineEdit):
                    value = valueWidget.text()
                    if not os.path.exists(value):
                        if "/" in value or "\\" in value:
                            print("can't find: " + value)
                            value = os.getcwd() + "/" + value
                elif isinstance(valueWidget, QComboBox):
                    value = valueWidget.currentText()
                
                keyValues[key] = value

        print(keyValues)

        return keyValues

    def getClazzWithRun(self, moduleString, args):
        ret = None

        try:
            # import file
            module = importlib.import_module("Plugins." + self.plugins[moduleString])
            # get class
            clazz  = getattr(module, moduleString)
            # new class
            obj = clazz(args)

            invert_op = getattr(obj, "start", None)
            if callable(invert_op):
                print(">>> enter plugin start method")
                if len(inspect.signature(invert_op).parameters) > 0:
                    ret = invert_op(args)
                else:
                    ret = invert_op()
                print("<<< end plugin start method")
        except Exception as e:
            print(e)

        if ret == None:
            return ""
        elif isinstance(ret, list):
            return "\n".join(ret)
        elif isinstance(ret, int) or isinstance(ret, float):
            return str(ret)
        else:
            return ret

    def PSRegexTemplateChanged(self):
        print("PSRegexTemplateChanged")
        regText = self.ui.PSRegexTemplateComboBox.currentText()
        self.config.setKeyValue("selectRegexTemplate", regText)

        for t in self.config.getValue("regexTemplate"):
            if t["name"] == regText:
                for key in t.keys():
                    if key == "name":
                        continue
                    if key == "value" or key == "regex":
                        self.ui.PSRegexPlainTextEdit.setPlainText(t[key])
                    if key == "xAxis":
                        self.ui.PSXAxisLineEdit.setText(", ".join([str(i) for i in t[key]]))
                    if key == "dataIndex":
                        self.ui.PSDataIndexLineEdit.setText(", ".join([str(i) for i in t[key]]))
                    if key == "plotType":
                        self.ui.PSPlotTypeComboBox.setCurrentText(t[key])

                break

    def PSPluginsChanged(self):
        pluginsIndex = self.ui.PSPluginsComboBox.currentIndex()

        # clear
        item_list = list(range(self.ui.PSGridLayout.count()))
        item_list.reverse()# 倒序删除，避免影响布局顺序

        for i in item_list:
            item = self.ui.PSGridLayout.itemAt(i)
            self.ui.PSGridLayout.removeItem(item)
            if item.widget():
                item.widget().deleteLater()

        # fill gridlayout
        self.fillPSGridLayout(self.ui.PSGridLayout, self.getClazzArgs(self.pluginsKeys[pluginsIndex]))

        self.config.setKeyValue("pluginIndex", self.ui.PSPluginsComboBox.currentIndex())

        print(self.pluginsKeys[pluginsIndex])

    def PSArgsComboxChanged(self):
        print("PSArgsComboxChanged")
        row, col = self.findWidgetPosition(self.ui.PSGridLayout)
        print("select: %d, %d" % (row, col))

        comboBox: QComboBox = self.ui.PSGridLayout.itemAtPosition(row, col).widget()
        print(comboBox.currentText())

    def getFiles(self, path) :
        for (dirpath, dirnames, filenames) in os.walk(path) :
            dirpath   = dirpath
            dirnames  = dirnames
            filenames = filenames
            return filenames

        return []

    def getPluginFiles(self, dirpath):
        plugins = self.getFiles(dirpath)
        print(plugins)
        # plugins.remove("__init__.py")
        plugins.sort()

        return plugins
