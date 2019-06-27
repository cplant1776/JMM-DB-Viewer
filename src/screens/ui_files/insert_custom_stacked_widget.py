# Standard Library Imports
import os.path
import subprocess
import sys
# Third Party Imports
# Local Imports

# ==============================================================
# Main
# ==============================================================
if __name__ == '__main__':
    """Converts ui file to py then replace stackedWidget from generated main_window.py with modified version"""

    # ===========================
    # Convert ui -> py
    # ===========================
    script_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'convert_to_py.ps1')
    # print(script_path)
    p = subprocess.Popen(['powershell.exe', '-File', r'{}'.format(script_path)],
                         stdout=sys.stdout, shell=True)
    p.communicate()

    # ===========================
    # Insert custom stackedWidget
    # ===========================
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
