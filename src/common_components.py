from typing import Callable

from PySide6 import QtCore, QtWidgets, QtGui
import resources


def construct_title(text: str, icon: str) -> QtWidgets.QHBoxLayout:
    title_horizontal_layout = QtWidgets.QHBoxLayout()
    title_button = QtWidgets.QPushButton()
    title_button.setText(" " + text)
    title_button.setIcon(resources.resources[icon])
    title_button.setIconSize(QtCore.QSize(48, 48))
    title_button.setStyleSheet("font-size: 28pt; border-radius: 5px;")
    title_horizontal_layout.addWidget(title_button)

    return title_horizontal_layout


def construct_subtitle(text: str) -> QtWidgets.QLabel:
    subtitle_label = QtWidgets.QLabel()
    subtitle_label.setText(text)
    subtitle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
    subtitle_label.setStyleSheet("margin-bottom: 20px; color: rgb(150, 150, 150); font-size: 12pt;")

    return subtitle_label

def construct_centered_button(text: str, icon: str, slot: Callable) -> QtWidgets.QHBoxLayout:
    button_horizontal_layout = QtWidgets.QHBoxLayout()
    button = QtWidgets.QPushButton()
    button.setText(text)

    if icon is not None:
        button.setText(" " + text + "   ")
        button.setIcon(resources.resources[icon])
        button.setIconSize(QtCore.QSize(28, 28))

    button.clicked.connect(slot)
    button.setStyleSheet("font-size: 12pt; margin-top: 10px;")
    button.setMinimumSize(QtCore.QSize(300, 80))
    button.setMaximumSize(QtCore.QSize(300, 80))
    button_horizontal_layout.addWidget(button)

    return button_horizontal_layout