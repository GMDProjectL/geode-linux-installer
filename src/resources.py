import os

from PySide6 import QtCore, QtWidgets, QtGui

dirpath = os.path.dirname(os.path.abspath(__file__))

resources = {
    'icon': None,
    'title': None
}

def load_icon():
    global resources
    icon_path = os.path.join(dirpath, "../assets/icon.png")
    resources['icon'] = QtGui.QIcon(icon_path)

def load_title():
    global resources
    title_path = os.path.join(dirpath, "../assets/title.png")
    resources['title'] = QtGui.QIcon(title_path)