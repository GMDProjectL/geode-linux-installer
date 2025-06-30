import sys
from PySide6 import QtWidgets, QtCore, QtGui

from installation_method_page import InstallationMethodPage
from welcome_page import WelcomePage
import resources

class MainWindow(QtWidgets.QMainWindow):
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

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    resources.load_resources()

    widget = MainWindow()
    widget.setWindowIcon(resources.resources['icon'])
    widget.setWindowTitle("Geode Linux Installer")
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())