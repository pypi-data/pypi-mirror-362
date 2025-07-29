#!/usr/bin/env python3

class AndroidSystemWakeup:
    """
    AndroidSystemWakeup类是一个编写LogTools插件的示例

    @name(AndroidSystemWakeup): 唯一码别名
    @path(input/0002_AndroidSystemWakeup.curf): 唯一码别名
    """

    def __init__(self, kwargs):
        print(">>> in plugin init method")

        print("AndroidSystemWakeup")

        print("<<< out plugin init method")

    # 装饰@PluginsPy.addRun自动添加run方法参考
    # @classmethod
    # def run(clazz, kwargs):
    #     print(">>> enter plugin run method")
    #     print(kwargs)
    #     clazz(kwargs)
    #     print("<<< end plugin run method")

    def start(self, kwargs):
        print(">>> in plugin start method")
        print(kwargs)
        print("<<< out plugin start method")

        return kwargs["name"]

if __name__ == "__main__" :
    AndroidSystemWakeup({})
