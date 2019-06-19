# Standard Library Imports
import os.path
# Third Party Imports
# Local Imports

# ==============================================================
# Main
# ==============================================================
if __name__ == '__main__':
    """Replace stackedWidget from ui generated main_window.py with modified version"""
    # Read main_window.py into memory
    main_window_path = os.path.join('..', 'main_window.py')
    with open(main_window_path, 'r') as in_file:
        buf = in_file.readlines()

    # Open output file
    with open(main_window_path, 'w+') as out_file:
        for line in buf:
            # Add local import
            if line == 'from PyQt5 import QtCore, QtGui, QtWidgets\n':
                line = line + 'from src.screens.screen_functions.stacked_widget_subclass import MyStackWidget\n'
            # Replace original stackedWidget with modified version
            elif line == '        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)\n':
                line = '        self.stackedWidget = MyStackWidget()\n'
            # Write line
            out_file.write(line)

    print("insert_custom_stacked_widget.py done!")
