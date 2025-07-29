#!/usr/bin/env python3

import subprocess
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import _thread
import queue
import re
import datetime
import os

def Shell(*cmd):
    out = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    data = out.stdout.read()
    if data != None:
        return data.decode('utf-8').strip()
    else:
        return ""

class DataLive:

    """
    利用MediaPipe绘制手掌

    """

    def __init__(self, kwargs):
        self.kwargs = kwargs
        self.frames = queue.Queue()
        self.parseDataRuning = False
        self.x = []
        self.y = []

        self.parseData()

    def parseData(self):
        print("DLParseData")

        if len(Shell("adb", "devices").split("\n")) > 1:
            _thread.start_new_thread(self.logcat, (self.capture, self.kwargs))
        else:
            print("please plugin your device")

    def runClick(self):
        print("DLRunClick")

        if len(Shell("adb", "devices").split("\n")) <= 1:
            print("please plugin your device")
            return

        if not self.parseDataRuning:
            self.parseData()

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')

        self.fig.canvas.mpl_connect('key_press_event', self.controller)
        self.ani = animation.FuncAnimation(self.fig, self.change_plot, interval=1000 / 10)

        plt.show()

    def controller(self, event):
        print('press', event.key)

        if event.key == "a":
            if self.parseDataRuning:
                self.parseDataRuning = False
                plt.close()

    def change_plot(self, args):
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
        self.ax.cla()

        while not self.frames.empty():
            frame = self.frames.get()
            print(frame)
            self.x.append(frame[0])
            self.y.append(frame[1])

        # self.ax.plot(self.x, [1] * len(self.x))
        self.ax.scatter(self.x, [1] * len(self.x))

        for i in range(len(self.x)):
            self.ax.text(self.x[i], 1 + 0.05, self.y[i], fontsize=9, rotation=90)
            self.ax.plot([self.x[i], self.x[i]], [1, 0], linestyle = 'dotted')

    def capture(self, line, config):
        for i in config["regex"]:
            datePattern       = re.compile(i)
            matchDatePattern  = datePattern.match(line)
            if matchDatePattern:
                lineInfo = self.defaultLineCallback(matchDatePattern.groups())
                print(lineInfo)
                self.frames.put(lineInfo)

    def defaultLineCallback(self, lineInfo):
        lineInfoFixed = []
        today_year    = str(datetime.date.today().year)
        # print(lineInfo)

        for index in range(len(lineInfo)):
            data       = None
            dateRegex  = "(\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2}\.\d*)"
            floatRegex = "[-]?\d*\.\d*"
            intRegex   = "[-]?\d+"

            datePattern       = re.compile(dateRegex)
            floatPattern      = re.compile(floatRegex)
            intPattern        = re.compile(intRegex)
            matchDatePattern  = datePattern.match(lineInfo[index])
            matchFloatPattern = floatPattern.match(lineInfo[index])
            matchIntPattern   = intPattern.match(lineInfo[index])

            if matchDatePattern:
                timeString = today_year + "-" + lineInfo[index]
                data = datetime.datetime.strptime(timeString, "%Y-%m-%d %H:%M:%S.%f")
            elif matchFloatPattern:
                data = eval("float(lineInfo[index].strip())")
            elif matchIntPattern:
                data = eval("int(lineInfo[index].strip())")
            else:
                data = lineInfo[index].strip()

            lineInfoFixed.append(data)

        return lineInfoFixed


    def logcat(self, func, config):
        cmd = config["cmd"]

        if "dmesg" in cmd:
            Shell("adb", "root")

        screenData = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

        while True:
            line = screenData.stdout.readline()

            if not self.parseDataRuning:
                print("exit parse data")
                break

            if line == b'' or subprocess.Popen.poll(screenData) == 0:
                screenData.stdout.close()
                break

            func(line.decode('utf-8').strip(), config)

if __name__ == "__main__":
    pass
