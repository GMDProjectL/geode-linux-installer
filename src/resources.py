import os

from PySide6 import QtGui

dirpath = os.path.dirname(os.path.abspath(__file__))

resources = {
    'icon': None,
    'title': None,
    'steam': None,
    'wine': None
}

def load_resource(name):
    global resources
    res_path = os.path.join(dirpath, f"../assets/{name}.png")
    resources[name] = QtGui.QIcon(res_path)

def load_resources():
    load_resource('icon')
    load_resource('title')
    load_resource('steam')
    load_resource('wine')