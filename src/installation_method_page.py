from typing import Callable

from PySide6 import QtCore, QtWidgets
from locales import i18n_get
import common_components

class InstallationMethodPage(QtWidgets.QWidget):

    steam_selected = QtCore.Signal()
    wine_selected = QtCore.Signal()

    def __init__(self):
        super().__init__()

        main_vertical_layout = QtWidgets.QVBoxLayout()

        top_spacer = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Expanding)
        main_vertical_layout.addItem(top_spacer)

        main_vertical_layout.addLayout(
            common_components.construct_title(
                i18n_get('installation_method_title'), 'icon'
            )
        )

        main_vertical_layout.addWidget(
            common_components.construct_subtitle(
                i18n_get('installation_method_subtitle')
            )
        )

        main_vertical_layout.addLayout(
            common_components.construct_centered_button(
                i18n_get('steam'), 'steam', self.steam_button_clicked
            )
        )

        main_vertical_layout.addLayout(
            common_components.construct_centered_button(
                i18n_get('wine'), 'wine', self.wine_button_clicked
            )
        )

        bottom_spacer = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Expanding)
        main_vertical_layout.addItem(bottom_spacer)

        self.setLayout(main_vertical_layout)

    @QtCore.Slot()
    def steam_button_clicked(self):
        self.steam_selected.emit()

    @QtCore.Slot()
    def wine_button_clicked(self):
        self.wine_selected.emit()
