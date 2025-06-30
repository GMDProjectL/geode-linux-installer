import os

from PySide6 import QtCore, QtWidgets, QtGui
import resources
import locale

class WelcomePage(QtWidgets.QWidget):

    install_clicked = QtCore.Signal()

    def __init__(self):
        super().__init__()

        resources.load_title()

        main_vertical_layout = QtWidgets.QVBoxLayout()

        top_spacer = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Expanding)
        main_vertical_layout.addItem(top_spacer)

        title_horizontal_layout = QtWidgets.QHBoxLayout()
        title_button = QtWidgets.QPushButton()
        title_button.setText(" " + locale.i18n_get('geode_for_linux'))
        title_button.setIcon(resources.resources['icon'])
        title_button.setIconSize(QtCore.QSize(48, 48))
        title_button.setStyleSheet("font-size: 28pt; border-radius: 5px;")
        title_horizontal_layout.addWidget(title_button)

        main_vertical_layout.addLayout(title_horizontal_layout)

        button_horizontal_layout = QtWidgets.QHBoxLayout()
        start_button = QtWidgets.QPushButton()
        start_button.setText("➡️  " + locale.i18n_get('install'))
        start_button.clicked.connect(self.install_clicked)
        start_button.setStyleSheet("font-size: 12pt; margin-top: 30px;")
        start_button.setMinimumSize(QtCore.QSize(300, 100))
        start_button.setMaximumSize(QtCore.QSize(300, 100))
        start_button.setIcon(QtGui.QIcon())

        button_horizontal_layout.addWidget(start_button)
        main_vertical_layout.addLayout(button_horizontal_layout)

        bottom_spacer = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Expanding)
        main_vertical_layout.addItem(bottom_spacer)

        disclaimer_text = QtWidgets.QLabel()
        disclaimer_text.setText(locale.i18n_get('disclaimer'))
        disclaimer_text.setStyleSheet("color: rgb(150, 150, 150); margin-bottom: 10px;")
        disclaimer_text.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        main_vertical_layout.addWidget(disclaimer_text)

        self.setLayout(main_vertical_layout)

    @QtCore.Slot()
    def start_button_clicked(self):
        self.install_clicked.emit()
