from PySide6 import QtCore, QtWidgets
from locales import i18n_get
import common_components

class WelcomePage(QtWidgets.QWidget):

    install_clicked = QtCore.Signal()

    def __init__(self):
        super().__init__()

        main_vertical_layout = QtWidgets.QVBoxLayout()

        top_spacer = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Expanding)
        main_vertical_layout.addItem(top_spacer)

        main_vertical_layout.addLayout(
            common_components.construct_title(
                i18n_get('geode_for_linux'), 'icon'
            )
        )

        main_vertical_layout.addWidget(
            common_components.construct_subtitle(
                i18n_get('geode_subtitle')
            )
        )

        main_vertical_layout.addLayout(
            common_components.construct_centered_button("➡️  " + i18n_get('install'), None,
                                                        self.start_button_clicked)
        )

        bottom_spacer = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Expanding)
        main_vertical_layout.addItem(bottom_spacer)

        disclaimer_text = QtWidgets.QLabel()
        disclaimer_text.setText(i18n_get('disclaimer'))
        disclaimer_text.setStyleSheet("color: rgb(150, 150, 150); margin-bottom: 10px;")
        disclaimer_text.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        main_vertical_layout.addWidget(disclaimer_text)

        self.setLayout(main_vertical_layout)

    @QtCore.Slot()
    def start_button_clicked(self):
        self.install_clicked.emit()
