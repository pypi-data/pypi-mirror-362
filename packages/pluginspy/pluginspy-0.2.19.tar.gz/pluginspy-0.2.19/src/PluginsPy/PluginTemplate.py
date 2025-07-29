from string import Template
from datetime import datetime
import os

class PluginTemplate:

    '''
    ${author}
    ${date}
    ${className}
    ${defaultArgs}
    ${instanceArgs}
    ${parseFilenames}
    ${regex}
    ${plotType}
    ${xAxis}
    ${dataIndex}
    '''

    DefaultKeys = [
        "author",
        "date",
        "className",
        "defaultArgs",
        "instanceArgs",
        "parseFilenames",
        "regex",
        "plotType",
        "xAxis",
        "dataIndex"
    ]

    def __init__(self, keyValues: dict):
        self.src = keyValues

    def setDefaultArgs(self, keyValues: dict):
        defaultArgs = ""
        instanceArgs  = ""
        parseFilenameArgs = []

        for key in keyValues.keys():
            if "/" in keyValues[key]:
                pathValue: str = keyValues[key]
                if os.getcwd() in pathValue:
                    pathValue = pathValue.replace(os.getcwd(), "").replace("\\", "/")[1:]

                defaultArgs += "    @" + key + "(" + pathValue + "): None\n"
                instanceArgs  += "        " + key + " = kwargs[\"" + key + "\"]\n"

                parseFilenameArgs.append(key)

        self.defaultArgs = defaultArgs.strip()
        self.instanceArgs = instanceArgs.strip()
        self.parseFilenames = ", ".join(parseFilenameArgs)

    def composite(self):

        for key in self.src.keys():
            if key == "author":
                self.author = self.src[key]
            if key == "className":
                self.className = self.src[key]
            if key == "defaultArgs":
                self.defaultArgs = self.src[key]
            if key == "instanceArgs":
                self.instanceArgs = self.src[key]
            if key == "parseFilenames":
                self.parseFilenames = ", ".join(self.src[key])
            if key == "regex":
                self.regex = "\n            '" + "',\n            '".join(self.src[key]) + "'\n            "
            if key == "plotType":
                self.plotType = self.src[key]
            if key == "xAxis":
                self.xAxis = (", ".join([str(i) for i in self.src[key]]))
            if key == "dataIndex":
                self.dataIndex = (", ".join([str(i) for i in self.src[key]]))
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.target = {}
        for key in PluginTemplate.DefaultKeys:
            try:
                exec('self.target["' + key + '"] = self.' + key)
            except:
                print("can't found: " + key + ", set to None")
                exec('self.target["' + key + '"] = ""')

        print(self.target)

    def parseTemplate(self, filePath = os.path.dirname(__file__) + "/assets/PluginTemplate.py"):
        with open(filePath, 'r') as f:
            template_str = f.read()
            t = Template(template_str)
            result = t.substitute(self.target)

            return result

if __name__ == "__main__" :
    pt = PluginTemplate(
        {
            "author": "zengjf",
            "className": "MediaPipeHands",
            "regex": ['x\s*=\s*([-]?\d.\d+),\s*y\s*=\s*([-]?\d.\d+),\s*z\s*=\s*([-]?\d.\d+)'],
            "plotType": "3D",
            "xAxis": [0],
            "dataIndex": [0, 1, 2]
        }
    )

    pt.setDefaultArgs({
        "data": "input/hands.txt",
        })
    pt.composite()
    print(pt.parseTemplate())
