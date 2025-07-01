#!/usr/bin/env python3
import os
import sys
from pathlib import Path

from PySide6 import QtWidgets, QtCore

from installation_method_page import InstallationMethodPage
from locales import i18n_get
from welcome_page import WelcomePage
import resources
import installation_utils

class MainWindow(QtWidgets.QMainWindow):
    worker_thread: installation_utils.WineInstallationThread | installation_utils.SteamInstallationThread = None
    progress_dialog: QtWidgets.QProgressDialog = None

    def __init__(self):
        super().__init__()

        self.stack_widget = QtWidgets.QStackedWidget(self)
        self.welcome_page = WelcomePage()
        self.stack_widget.addWidget(self.welcome_page)
        self.stack_widget.setCurrentWidget(self.welcome_page)

        self.welcome_page.install_clicked.connect(self.install_clicked)

        self.setCentralWidget(self.stack_widget)

    @QtCore.Slot()
    def install_clicked(self):
        installation_method_page = InstallationMethodPage()
        self.stack_widget.addWidget(installation_method_page)
        self.stack_widget.setCurrentWidget(installation_method_page)
        installation_method_page.steam_selected.connect(self.steam_selected)
        installation_method_page.wine_selected.connect(self.wine_selected)

    @QtCore.Slot()
    def steam_selected(self):
        self.worker_thread = installation_utils.SteamInstallationThread()
        self.start_installation_worker('Steam')

    @QtCore.Slot()
    def wine_selected(self):
        wineprefix = Path(os.getenv('WINEPREFIX', f'{os.getenv('HOME')}/.wine'))
        prefix_question: QtWidgets.QDialogButtonBox.StandardButton = QtWidgets.QMessageBox.question(
            self, '',
            i18n_get('wine_select_prefix').format(wineprefix),
            QtWidgets.QMessageBox.StandardButton.Yes, QtWidgets.QMessageBox.StandardButton.No
        )

        if prefix_question == QtWidgets.QMessageBox.StandardButton.No:
            wineprefix = QtWidgets.QFileDialog.getExistingDirectory(self, i18n_get('wine_select_prefix_caption'))
            if wineprefix == '':
                QtWidgets.QMessageBox.warning(self, '', i18n_get('wine_prefix_is_not_selected'))
                return

        QtWidgets.QMessageBox.information(self, '', i18n_get('wine_select_gd_dir'))

        gd_dir = QtWidgets.QFileDialog.getExistingDirectory(self, i18n_get('wine_select_gd_caption'))

        if gd_dir == '':
            QtWidgets.QMessageBox.warning(self, '', i18n_get('wine_gd_dir_is_not_selected'))
            return

        self.worker_thread = installation_utils.WineInstallationThread(Path(wineprefix), Path(gd_dir))
        self.start_installation_worker('Wine')

    def start_installation_worker(self, method: str):
        self.worker_thread.finished_signal.connect(self.installation_done)
        self.worker_thread.start()

        self.progress_dialog = QtWidgets.QProgressDialog(
            i18n_get('installing_text').format(method), None, 0, 0, self
        )
        self.progress_dialog.setWindowTitle(i18n_get('installing_title'))
        self.progress_dialog.setModal(True)
        self.progress_dialog.setMinimumDuration(0)
        self.progress_dialog.setCancelButton(None)
        self.progress_dialog.show()

    @QtCore.Slot()
    def installation_done(self, success: bool, message: str):
        self.progress_dialog.hide()

        if success:
            QtWidgets.QMessageBox.information(self, "", i18n_get('installation_successful'))
        else:
            QtWidgets.QMessageBox.critical(self, "", i18n_get('installation_failed').format(message))

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    app.setApplicationName("geode-linux-installer")
    app.setOrganizationName("relative")
    app.setApplicationDisplayName("Geode Linux Installer")

    resources.load_resources()

    widget = MainWindow()
    widget.setWindowIcon(resources.resources['icon'])
    widget.setWindowTitle("Geode Linux Installer")
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())