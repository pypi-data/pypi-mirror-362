#!/usr/bin/env python3

class PluginExample:
    """
    PluginExample类是一个编写LogTools插件的示例

    @id(123456): 唯一码
    @name(zengjf): 唯一码别名
    """

    def __init__(self, kwargs):
        print(">>> in plugin init method")

        self.id = kwargs["id"]
        self.name = kwargs["name"]

        print("实例输出：id: " + kwargs["id"] + ", name: " + kwargs["name"])

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

if __name__ == "__main__" :
    PluginExample({"id": "123456", "name": "zengjf"})
