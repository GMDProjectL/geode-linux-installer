import sys
from PySide6 import QtWidgets, QtCore, QtGui
from welcome_page import WelcomePage
import resources

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        stack_widget = QtWidgets.QStackedWidget(self)
        self.welcome_page = WelcomePage()
        stack_widget.addWidget(self.welcome_page)
        stack_widget.setCurrentWidget(self.welcome_page)

        self.welcome_page.install_clicked.connect(self.install_clicked)

        self.setCentralWidget(stack_widget)

    @QtCore.Slot()
    def install_clicked(self):
        QtWidgets.QMessageBox.information(self, "Welcome Page", "Welcome Page")

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    resources.load_icon()

    widget = MainWindow()
    widget.setWindowIcon(resources.resources['icon'])
    widget.setWindowTitle("Geode Linux Installer")
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())