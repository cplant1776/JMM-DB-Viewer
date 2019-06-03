# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!


# Standard Library Imports
from functools import partial
# Third Party Imports
from PyQt5 import QtCore, QtGui, QtWidgets
# Local Imports
from src.config import SETTINGS
from src.db_con import DBCon
from src.screens.screen_functions.stacked_widget_subclass import MyStackWidget


class Ui_MainWindow(object):

    def __init__(self):
        self.db_con = DBCon(db_loc=SETTINGS['local_database_path'])

    def bind_buttons(self):
        self.search_btn.clicked.connect(partial(self.stackedWidget.go_to_screen, screen='search'))
        self.serialized_btn.clicked.connect(partial(self.stackedWidget.go_to_screen, screen='serial'))
        self.back_btn_search_result.clicked.connect(partial(self.stackedWidget.go_to_previous_screen))
        self.submit_search_btn.clicked.connect(partial(self.run_search))
        self.back_btn_serial.clicked.connect(partial(self.stackedWidget.go_to_previous_screen))
        # self.layaway_btn.clicked.connect(self.run_search)

    def run_search(self):

        # Run appropriate query and store result
        is_general_search = False
        if self.general_radio.isChecked():
            term = (self.general_search.text(),)
            print("General search: {}".format(term[0]))
            result = self.db_con.general_search(term)
            is_general_search = True
        elif self.first_radio.isChecked():
            first = self.first_search.text()
            print("First name search: {}".format(first))
            result = self.db_con.search_by_first_name(first)
        elif self.last_radio.isChecked():
            last = self.last_search.text()
            print("Last name search: {}".format(last))
            result = self.db_con.search_by_last_name(last)
        elif self.phone_radio.isChecked():
            num = self.phone_search.text()
            print("Phone search: {}".format(num))
            result = self.db_con.search_by_number(num)

        self.populate_search_result(result=result, is_general_search=is_general_search)
        self.stackedWidget.go_to_screen(screen='search_result')

    def populate_search_result(self, result, is_general_search=False):
        if is_general_search:
            # TODO: Implement general result screen for deciding which data to list
            pass
        else:
            self.search_result_table.setRowCount(len(result))
            for row, r in enumerate(result):
                for col, item in enumerate(r):
                    self.search_result_table.setItem(row, col, QtWidgets.QTableWidgetItem(item))

    def setupUi(self, MainWindow):

        # =================================================================================
        #  MAIN WINDOW
        # =================================================================================

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1076, 869)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.stackedWidget = MyStackWidget()
        self.stackedWidget.setFrameShape(QtWidgets.QFrame.Box)
        self.stackedWidget.setObjectName("stackedWidget")

        # =================================================================================
        #  Start Page
        # =================================================================================

        self.start_page = QtWidgets.QWidget()
        self.start_page.setObjectName("start_page")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.start_page)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)

        # Search Button
        self.search_btn = QtWidgets.QPushButton(self.start_page)
        self.search_btn.setObjectName("search_btn")
        self.gridLayout.addWidget(self.search_btn, 1, 1, 1, 1)
        # self.search_btn.clicked.connect(partial(self.stackedWidget.go_to_screen, screen='search'))

        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 2, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 2, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 2, 2, 1, 1)

        # Serialized Inventory Button
        self.serialized_btn = QtWidgets.QPushButton(self.start_page)
        self.serialized_btn.setObjectName("serialized_btn")
        self.gridLayout.addWidget(self.serialized_btn, 3, 1, 1, 1)
        # self.serialized_btn.clicked.connect(partial(self.stackedWidget.go_to_screen, screen='serial'))


        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem4, 4, 1, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.start_page)

        # =================================================================================
        #  Search Results Page
        # =================================================================================
        self.search_result_page = QtWidgets.QWidget()
        self.search_result_page.setObjectName("search_result_page")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.search_result_page)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")

        # Back Button
        self.back_btn_search_result = QtWidgets.QPushButton(self.search_result_page)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.back_btn_search_result.sizePolicy().hasHeightForWidth())
        self.back_btn_search_result.setSizePolicy(sizePolicy)
        self.back_btn_search_result.setObjectName("back_btn_search_result")
        self.gridLayout_2.addWidget(self.back_btn_search_result, 1, 1, 1, 1)


        # Search Result Table
        self.search_result_table = QtWidgets.QTableWidget(self.search_result_page)
        self.search_result_table.setObjectName("search_result_table")
        self.search_result_table.setColumnCount(8)
        self.search_result_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.search_result_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.search_result_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.search_result_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.search_result_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.search_result_table.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.search_result_table.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.search_result_table.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.search_result_table.setHorizontalHeaderItem(7, item)

        self.gridLayout_2.addWidget(self.search_result_table, 0, 0, 1, 3)
        spacerItem5 = QtWidgets.QSpacerItem(353, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem5, 1, 0, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(353, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem6, 1, 2, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.search_result_page)

        # =================================================================================
        #  Search Page
        # =================================================================================
        self.search_page = QtWidgets.QWidget()
        self.search_page.setObjectName("search_page")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.search_page)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_6.addItem(spacerItem7, 0, 1, 1, 1)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem8, 1, 0, 1, 1)
        self.gridLayout_7 = QtWidgets.QGridLayout()
        self.gridLayout_7.setObjectName("gridLayout_7")

        # General Search Radio Button
        self.general_radio = QtWidgets.QRadioButton(self.search_page)
        self.general_radio.setText("")
        self.general_radio.setObjectName("general_radio")
        self.gridLayout_7.addWidget(self.general_radio, 7, 0, 1, 2)
        self.label_4 = QtWidgets.QLabel(self.search_page)
        self.label_4.setObjectName("label_4")
        self.gridLayout_7.addWidget(self.label_4, 0, 2, 1, 1, QtCore.Qt.AlignHCenter)

        # Submit Search Button
        self.submit_search_btn = QtWidgets.QPushButton(self.search_page)
        self.submit_search_btn.setObjectName("submit_search_btn")
        self.gridLayout_7.addWidget(self.submit_search_btn, 8, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.search_page)
        self.label_5.setObjectName("label_5")
        self.gridLayout_7.addWidget(self.label_5, 4, 2, 1, 1, QtCore.Qt.AlignHCenter)
        # self.submit_search_btn.clicked.connect(self.stackedWidget.run_search)

        # General Search Field
        self.general_search = QtWidgets.QLineEdit(self.search_page)
        self.general_search.setText("")
        self.general_search.setObjectName("general_search")
        self.gridLayout_7.addWidget(self.general_search, 7, 2, 1, 1)

        self.label_6 = QtWidgets.QLabel(self.search_page)
        self.label_6.setObjectName("label_6")
        self.gridLayout_7.addWidget(self.label_6, 6, 2, 1, 1, QtCore.Qt.AlignHCenter)

        # Last Name Search
        self.last_search = QtWidgets.QLineEdit(self.search_page)
        self.last_search.setText("")
        self.last_search.setObjectName("last_search")
        self.gridLayout_7.addWidget(self.last_search, 5, 1, 1, 2)

        # Phone Number Search Field
        self.phone_search = QtWidgets.QLineEdit(self.search_page)
        self.phone_search.setText("")
        self.phone_search.setObjectName("phone_search")
        self.gridLayout_7.addWidget(self.phone_search, 1, 1, 1, 2)

        # Phone Number Radio Button
        self.phone_radio = QtWidgets.QRadioButton(self.search_page)
        self.phone_radio.setText("")
        self.phone_radio.setObjectName("phone_radio")
        self.gridLayout_7.addWidget(self.phone_radio, 1, 0, 1, 1)

        # Last Name Radio Button
        self.last_radio = QtWidgets.QRadioButton(self.search_page)
        self.last_radio.setText("")
        self.last_radio.setObjectName("last_radio")
        self.gridLayout_7.addWidget(self.last_radio, 5, 0, 1, 1)

        # First Name Radio Button
        self.first_radio = QtWidgets.QRadioButton(self.search_page)
        self.first_radio.setText("")
        self.first_radio.setObjectName("first_radio")
        self.gridLayout_7.addWidget(self.first_radio, 3, 0, 1, 1)

        # First Name Search Field
        self.first_search = QtWidgets.QLineEdit(self.search_page)
        self.first_search.setText("")
        self.first_search.setObjectName("first_search")
        self.gridLayout_7.addWidget(self.first_search, 3, 1, 1, 2)

        self.label_7 = QtWidgets.QLabel(self.search_page)
        self.label_7.setObjectName("label_7")
        self.gridLayout_7.addWidget(self.label_7, 2, 2, 1, 1, QtCore.Qt.AlignHCenter)
        self.gridLayout_6.addLayout(self.gridLayout_7, 1, 1, 1, 1)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem9, 1, 2, 1, 1)
        spacerItem10 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_6.addItem(spacerItem10, 2, 1, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_6, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.search_page)


        # =================================================================================
        #  Serialized Inventory Page
        # =================================================================================

        self.serialized_page = QtWidgets.QWidget()
        self.serialized_page.setObjectName("serialized_page")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.serialized_page)
        self.gridLayout_8.setObjectName("gridLayout_8")

        # Serialized Inventory Table
        self.serial_table = QtWidgets.QTableWidget(self.serialized_page)
        self.serial_table.setObjectName("serial_table")
        self.serial_table.setColumnCount(5)
        self.serial_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.serial_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.serial_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.serial_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.serial_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.serial_table.setHorizontalHeaderItem(4, item)
        self.gridLayout_8.addWidget(self.serial_table, 0, 0, 1, 3)

        spacerItem11 = QtWidgets.QSpacerItem(404, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_8.addItem(spacerItem11, 1, 0, 1, 1)

        # Back Button
        self.back_btn_serial = QtWidgets.QPushButton(self.serialized_page)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.back_btn_serial.sizePolicy().hasHeightForWidth())
        self.back_btn_serial.setSizePolicy(sizePolicy)
        self.back_btn_serial.setMinimumSize(QtCore.QSize(200, 0))
        self.back_btn_serial.setMaximumSize(QtCore.QSize(200, 16777215))
        self.back_btn_serial.setObjectName("back_btn_serial")
        self.gridLayout_8.addWidget(self.back_btn_serial, 1, 1, 1, 1)
        # self.back_btn_serial.clicked.connect(self.stackedWidget.go_to_previous_screen)

        spacerItem12 = QtWidgets.QSpacerItem(406, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_8.addItem(spacerItem12, 1, 2, 1, 1)
        self.stackedWidget.addWidget(self.serialized_page)

        # =================================================================================
        #  Service Request Order (SRO) Page
        # =================================================================================
        self.sro_page = QtWidgets.QWidget()
        self.sro_page.setObjectName("sro_page")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.sro_page)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        # SRO Data Table
        self.data_table_3 = QtWidgets.QTableWidget(self.sro_page)
        self.data_table_3.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.data_table_3.sizePolicy().hasHeightForWidth())
        self.data_table_3.setSizePolicy(sizePolicy)
        self.data_table_3.setMaximumSize(QtCore.QSize(16777215, 308))
        self.data_table_3.setObjectName("data_table_3")
        self.data_table_3.setColumnCount(1)
        self.data_table_3.setRowCount(7)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.data_table_3.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.data_table_3.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.data_table_3.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.data_table_3.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.data_table_3.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.data_table_3.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.data_table_3.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.data_table_3.setHorizontalHeaderItem(0, item)
        self.horizontalLayout_3.addWidget(self.data_table_3)

        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_8 = QtWidgets.QLabel(self.sro_page)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_3.addWidget(self.label_8)

        # Service Request Notes
        self.service_text = QtWidgets.QTextBrowser(self.sro_page)
        self.service_text.setObjectName("service_text")
        self.verticalLayout_3.addWidget(self.service_text)
        self.label_9 = QtWidgets.QLabel(self.sro_page)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_3.addWidget(self.label_9)

        # Work Done Notes
        self.work_text = QtWidgets.QTextBrowser(self.sro_page)
        self.work_text.setObjectName("work_text")
        self.verticalLayout_3.addWidget(self.work_text)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.gridLayout_9.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)
        self.layoutWidget_3 = QtWidgets.QWidget(self.sro_page)
        self.layoutWidget_3.setGeometry(QtCore.QRect(270, 140, 193, 31))
        self.layoutWidget_3.setObjectName("layoutWidget_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.layoutWidget_3)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem13 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem13)
        self.back_btn_3 = QtWidgets.QPushButton(self.layoutWidget_3)
        self.back_btn_3.setObjectName("back_btn_3")
        self.horizontalLayout_4.addWidget(self.back_btn_3)
        spacerItem14 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem14)
        self.stackedWidget.addWidget(self.sro_page)

        # =================================================================================
        #  Customer Page
        # =================================================================================
        self.customer_page = QtWidgets.QWidget()
        self.customer_page.setObjectName("customer_page")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.customer_page)
        self.gridLayout_10.setObjectName("gridLayout_10")
        spacerItem15 = QtWidgets.QSpacerItem(368, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_10.addItem(spacerItem15, 0, 0, 1, 1)

        # Customer Table 1 - ID/First/Last/Company/Email
        self.customer_table_1 = QtWidgets.QTableWidget(self.customer_page)
        self.customer_table_1.setMaximumSize(QtCore.QSize(251, 231))
        self.customer_table_1.setObjectName("customer_table_1")
        self.customer_table_1.setColumnCount(1)
        self.customer_table_1.setRowCount(5)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.customer_table_1.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.customer_table_1.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.customer_table_1.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.customer_table_1.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.customer_table_1.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.customer_table_1.setHorizontalHeaderItem(0, item)
        self.gridLayout_10.addWidget(self.customer_table_1, 0, 1, 1, 1)


        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.customer_table_2 = QtWidgets.QTableWidget(self.customer_page)
        self.customer_table_2.setMaximumSize(QtCore.QSize(241, 231))

        # Customer Table 2 - Addr/City/ST/Zip/Last Activity
        self.customer_table_2.setObjectName("customer_table_2")
        self.customer_table_2.setColumnCount(1)
        self.customer_table_2.setRowCount(5)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.customer_table_2.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.customer_table_2.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.customer_table_2.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.customer_table_2.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.customer_table_2.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.customer_table_2.setHorizontalHeaderItem(0, item)
        self.horizontalLayout_7.addWidget(self.customer_table_2)

        # Layaway Button
        self.layaway_btn = QtWidgets.QPushButton(self.customer_page)
        self.layaway_btn.setMaximumSize(QtCore.QSize(151, 121))
        self.layaway_btn.setObjectName("layaway_btn")
        self.horizontalLayout_7.addWidget(self.layaway_btn)
        # self.layaway_btn.clicked.connect(partial(self.stackedWidget.go_to_screen, screen='search_result'))

        spacerItem16 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem16)
        self.gridLayout_10.addLayout(self.horizontalLayout_7, 0, 2, 1, 2)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_10 = QtWidgets.QLabel(self.customer_page)
        self.label_10.setObjectName("label_10")
        self.verticalLayout_6.addWidget(self.label_10)

        # Phone Numbers Table
        self.phone_tbox = QtWidgets.QTableWidget(self.customer_page)
        self.phone_tbox.setMinimumSize(QtCore.QSize(0, 71))
        self.phone_tbox.setObjectName("phone_tbox")
        self.phone_tbox.setColumnCount(0)
        self.phone_tbox.setRowCount(0)

        self.verticalLayout_6.addWidget(self.phone_tbox)
        self.gridLayout_10.addLayout(self.verticalLayout_6, 1, 0, 1, 2)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_12 = QtWidgets.QLabel(self.customer_page)
        self.label_12.setObjectName("label_12")
        self.verticalLayout_5.addWidget(self.label_12)

        # Customer Notes Text Box
        self.notes_tbox = QtWidgets.QTextBrowser(self.customer_page)
        self.notes_tbox.setObjectName("notes_tbox")
        self.verticalLayout_5.addWidget(self.notes_tbox)
        self.gridLayout_10.addLayout(self.verticalLayout_5, 1, 2, 1, 2)

        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_13 = QtWidgets.QLabel(self.customer_page)
        self.label_13.setObjectName("label_13")
        self.verticalLayout_7.addWidget(self.label_13)

        # Transactions Table
        self.transactions_table = QtWidgets.QTableWidget(self.customer_page)
        self.transactions_table.setMinimumSize(QtCore.QSize(521, 0))
        self.transactions_table.setObjectName("transactions_table")
        self.transactions_table.setColumnCount(4)
        self.transactions_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.transactions_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.transactions_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.transactions_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.transactions_table.setHorizontalHeaderItem(3, item)

        self.verticalLayout_7.addWidget(self.transactions_table)
        self.gridLayout_10.addLayout(self.verticalLayout_7, 2, 0, 1, 3)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_11 = QtWidgets.QLabel(self.customer_page)
        self.label_11.setObjectName("label_11")
        self.verticalLayout_4.addWidget(self.label_11)

        # SRO Table
        self.sro_table = QtWidgets.QTableWidget(self.customer_page)
        self.sro_table.setMaximumSize(QtCore.QSize(401, 16777215))
        self.sro_table.setObjectName("sro_table")
        self.sro_table.setColumnCount(3)
        self.sro_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.sro_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.sro_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.sro_table.setHorizontalHeaderItem(2, item)
        self.verticalLayout_4.addWidget(self.sro_table)
        self.gridLayout_10.addLayout(self.verticalLayout_4, 2, 3, 1, 1)

        self.stackedWidget.addWidget(self.customer_page)
        self.horizontalLayout_2.addWidget(self.stackedWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1076, 27))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)


        # Retranslate UI & connect signals
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.search_btn.setText(_translate("MainWindow", "Run a Search"))
        self.serialized_btn.setText(_translate("MainWindow", "See Serialized Inventory"))
        self.back_btn_search_result.setText(_translate("MainWindow", "Back"))
        item = self.search_result_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "id"))
        item = self.search_result_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Last"))
        item = self.search_result_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "First"))
        item = self.search_result_table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Address"))
        item = self.search_result_table.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "City"))
        item = self.search_result_table.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "State"))
        item = self.search_result_table.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Zip"))
        item = self.search_result_table.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "Home Phone"))
        self.label_4.setText(_translate("MainWindow", "Phone #"))
        self.submit_search_btn.setText(_translate("MainWindow", "Search"))
        self.label_5.setText(_translate("MainWindow", "Last Name"))
        self.label_6.setText(_translate("MainWindow", "General Search"))
        self.label_7.setText(_translate("MainWindow", "First Name"))
        item = self.serial_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Make"))
        item = self.serial_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Model"))
        item = self.serial_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Serial #"))
        item = self.serial_table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Date"))
        item = self.serial_table.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Notes"))
        self.back_btn_serial.setText(_translate("MainWindow", "Back"))
        item = self.data_table_3.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "Service ID"))
        item = self.data_table_3.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "Customer ID"))
        item = self.data_table_3.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "Make"))
        item = self.data_table_3.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "Model"))
        item = self.data_table_3.verticalHeaderItem(4)
        item.setText(_translate("MainWindow", "Date In"))
        item = self.data_table_3.verticalHeaderItem(5)
        item.setText(_translate("MainWindow", "Finished On"))
        item = self.data_table_3.verticalHeaderItem(6)
        item.setText(_translate("MainWindow", "Picked Up"))
        item = self.data_table_3.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Value"))
        self.label_8.setText(_translate("MainWindow", "Service Request"))
        self.label_9.setText(_translate("MainWindow", "Work Performed"))
        self.back_btn_3.setText(_translate("MainWindow", "Back"))
        item = self.customer_table_1.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "Customer ID"))
        item = self.customer_table_1.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "First"))
        item = self.customer_table_1.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "Last"))
        item = self.customer_table_1.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "Company"))
        item = self.customer_table_1.verticalHeaderItem(4)
        item.setText(_translate("MainWindow", "Email"))
        item = self.customer_table_1.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Values"))
        item = self.customer_table_2.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "Address"))
        item = self.customer_table_2.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "City"))
        item = self.customer_table_2.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "State"))
        item = self.customer_table_2.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "Zip"))
        item = self.customer_table_2.verticalHeaderItem(4)
        item.setText(_translate("MainWindow", "Last Activity"))
        item = self.customer_table_2.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Values"))
        self.layaway_btn.setText(_translate("MainWindow", "Layaways"))
        self.label_10.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Potential Phones</span></p></body></html>"))
        self.label_12.setText(_translate("MainWindow", "Notes"))
        self.label_13.setText(_translate("MainWindow", "Transactions"))
        item = self.transactions_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Date"))
        item = self.transactions_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Subtotal"))
        item = self.transactions_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Tax"))
        item = self.transactions_table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Total"))
        self.label_11.setText(_translate("MainWindow", "SRO"))
        item = self.sro_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Date In"))
        item = self.sro_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Date Done"))
        item = self.sro_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Picked Up"))

