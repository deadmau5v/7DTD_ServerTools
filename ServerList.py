import json
import os
from xml.dom.minidom import Element
from xml.dom.minidom import parse

# 默认配置文件
default_config: Element = parse('default_config.xml').documentElement
for i in default_config.getElementsByTagName('property'):
    if i.getAttribute("name") == "ServerName":
        print(i.getAttribute("value"))


class ServerList:
    def __init__(self):
        # 判断配置文件是否存在
        if not os.path.exists('ServerList.json'):
            with open('ServerList.json', 'w') as f:
                f.write('''{
                    "ServerList": []
                }''')
        with open('ServerList.json', 'r') as f:
            self.server_list = json.load(f)['ServerList']

    def add(self, name, path):
        # 相对路径转为绝对路径
        path = os.path.abspath(path)
        # 路径是否存在
        if not os.path.exists(path):
            return False, "路径不存在"
        # 路径是否为文件夹
        if not os.path.isdir(path):
            return False, "路径不是文件夹"

        for i in self.server_list:
            if i['name'] == name:
                return False, "服务器名重复"
        self.server_list.append({
            "name": name,
            "path": path
        })

        # 在目标位置写入配置文件
        with open(path + os.sep + '7ServerTools.json', 'w') as f:
            f.write(f'''{
            "ServerName": {name},
                }''')

        return True, "添加成功"

    def delete(self, name):
        for i in self.server_list:
            if i['name'] == name:
                self.server_list.remove(i)
                break
