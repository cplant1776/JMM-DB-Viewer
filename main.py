import sys
from PyQt5 import QtWidgets

from src.screens.main_window import Ui_MainWindow
# from screens.transaction_screen import TransactionScreen
# from screens.screen_functions.start_screen import add_start_screen_widgets

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(w)
    # add_start_screen_widgets(ui)
    w.show()
    sys.exit(app.exec_())
