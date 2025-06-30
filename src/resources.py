import os

from PySide6 import QtCore, QtWidgets, QtGui

dirpath = os.path.dirname(os.path.abspath(__file__))

resources = {
    'icon': None,
    'title': None,
    'steam': None
}

def load_icon():
    global resources
    icon_path = os.path.join(dirpath, "../assets/icon.png")
    resources['icon'] = QtGui.QIcon(icon_path)

def load_title():
    global resources
    title_path = os.path.join(dirpath, "../assets/title.png")
    resources['title'] = QtGui.QIcon(title_path)

def load_steam():
    global resources
    steam_path = os.path.join(dirpath, "../assets/steam.png")
    resources['steam'] = QtGui.QIcon(steam_path)

def load_wine():
    global resources
    wine_path = os.path.join(dirpath, "../assets/wine.png")
    resources['wine'] = QtGui.QIcon(wine_path)

def load_resources():
    load_icon()
    load_title()
    load_steam()
    load_wine()