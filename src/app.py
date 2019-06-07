# Standard Library Imports
import sys
# Third Party Imports
from PyQt5 import QtWidgets
# Local Imports
from src.screens.master_window import MasterWindow
from src.config import SETTINGS


class App:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.main_window = self.setup_main_window()
        self.main_window.show()

    @staticmethod
    def setup_main_window():
        main_window = QtWidgets.QMainWindow()
        ui = MasterWindow()
        ui.setupUi(main_window)
        ui.bind_buttons()
        return main_window


# ==============================================================
# Main
# ==============================================================
if __name__ == '__main__':
    pass
