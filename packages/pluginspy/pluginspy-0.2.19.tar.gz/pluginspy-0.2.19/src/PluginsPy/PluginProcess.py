import multiprocessing
import importlib
import inspect
import re
import traceback
import time
from PyQt5.QtCore import QThread

def getClazzWithRun(moduleString, sender, args):
    ret = None
    module = None

    try:
        if moduleString == "VisualLogPlot":
            # import file
            module = importlib.import_module("PluginsPy." + moduleString)
        else:
            # import file
            module = importlib.import_module("Plugins." + moduleString)

        matchObj     = re.match(r'\d{4}[_]?', moduleString)
        if matchObj:
            moduleString = moduleString.replace(matchObj.group(0), "")

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
        traceback.print_exc()

    sendString = ""
    if ret == None:
        sendString = ""
    elif isinstance(ret, list):
        sendString = "\n".join(ret)
    elif isinstance(ret, int) or isinstance(ret, float):
        sendString = str(ret)
    elif isinstance(ret, str):
        sendString = str(ret)
    else:
        sendString = ""

    if sender != None:
        sender.send(sendString)
    else:
        return sendString

# class PluginProcess(threading.Thread):
class PluginProcess(QThread):

    def __init__(self, moduleString, kwargs, callback=None):
        super().__init__()
        self.moduleString = moduleString
        self.kwargs = kwargs
        self.processRetString = ""
        self.callback = callback

    def run(self):
        print("PluginProcess running")

        connRecv, connSend =  multiprocessing.Pipe()
        p = multiprocessing.Process(target=getClazzWithRun, args=(self.moduleString, connSend, self.kwargs, ))
        p.start()

        connSend.close()

        while p.is_alive():
            try:
                self.processRetString += connRecv.recv()
            except EOFError:
                break  # Occurs when the child connection is closed
            time.sleep(0.1)  # To avoid busy waiting

        print("Process ret: " + self.processRetString)

        if self.callback != None:
            self.callback(self.processRetString)

        p.join()
