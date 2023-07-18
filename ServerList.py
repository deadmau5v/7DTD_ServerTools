import json
import os
import time
from xml.dom.minidom import Element
from xml.dom.minidom import parse


def read_config(file, key):
    default_config: Element = parse(file).documentElement
    for i in default_config.getElementsByTagName('property'):
        if i.getAttribute("name") == key:
            return i.getAttribute("value")


def write_config(file, key, value):
    default_config: Element = parse(file).documentElement
    for i in default_config.getElementsByTagName('property'):
        if i.getAttribute("name") == key:
            i.setAttribute("value", value)
            break
    with open(file, 'w', encoding="utf-8") as f:
        default_config.writexml(f)


def new_config():
    with open('ServerList.json', 'w', encoding="utf-8") as f:
        f.write('''{
            "ServerList": []
        }''')


class ServerList:
    def __init__(self):

        # 判断配置文件是否存在
        if not os.path.exists('ServerList.json'):
            new_config()
        with open('ServerList.json', 'r', encoding="utf-8") as f:
            try:
                self.server_list = json.load(f)['ServerList']
            except json.decoder.JSONDecodeError:
                new_config()
                self.server_list = json.load(f)['ServerList']

    def add(self, name, path):
        # 判断服务器名是否重复
        for i in self.server_list:
            if i['name'] == name:
                return False, "服务器名重复"
        # 相对路径转为绝对路径
        path = os.path.abspath(path)
        # 路径是否存在
        if not os.path.exists(path):
            os.mkdir(path)
        # 路径是否为文件夹
        if not os.path.isdir(path):
            return False, "路径不是文件夹"

        for i in self.server_list:
            if i['name'] == name:
                return False, "服务器名重复"
        # 复制默认配置文件到文件夹
        os.system("cp -r default_config.xml " + path)

        self.server_list.append({
            "name": name,
            "path": path
        })
        # 修改默认配置文件
        write_config(path + "/default_config.xml", "ServerName", name)
        # 将 server_list 保存到 json 文件
        with open('ServerList.json', 'w', encoding="utf-8") as f:
            json.dump({"ServerList": self.server_list}, f)
        return True, "添加成功"

    def delete(self, name):
        for i in self.server_list:
            if i['name'] == name:
                path = i["path"]
                self.server_list.remove(i)
                break
        else:
            return False, "服务器不存在"
        # 将 server_list 保存到 json 文件
        with open('ServerList.json', 'w', encoding="utf-8") as f:
            json.dump({"ServerList": self.server_list}, f)
        # 删除文件夹
        os.system("rm -rf " + path)
        return True, "删除成功"

