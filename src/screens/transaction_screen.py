# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'transaction_screen.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class TransactionScreen(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(973, 802)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.transaction_table_1 = QtWidgets.QTableWidget(self.centralwidget)
        self.transaction_table_1.setMaximumSize(QtCore.QSize(261, 151))
        self.transaction_table_1.setObjectName("transaction_table_1")
        self.transaction_table_1.setColumnCount(1)
        self.transaction_table_1.setRowCount(3)
        item = QtWidgets.QTableWidgetItem()
        self.transaction_table_1.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.transaction_table_1.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.transaction_table_1.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.transaction_table_1.setHorizontalHeaderItem(0, item)
        self.gridLayout.addWidget(self.transaction_table_1, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(442, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.transaction_table_2 = QtWidgets.QTableWidget(self.centralwidget)
        self.transaction_table_2.setMaximumSize(QtCore.QSize(231, 111))
        self.transaction_table_2.setObjectName("transaction_table_2")
        self.transaction_table_2.setColumnCount(1)
        self.transaction_table_2.setRowCount(2)
        item = QtWidgets.QTableWidgetItem()
        self.transaction_table_2.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.transaction_table_2.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.transaction_table_2.setHorizontalHeaderItem(0, item)
        self.gridLayout.addWidget(self.transaction_table_2, 0, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 278, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 1, 0, 1, 1)
        self.transaction_table_4 = QtWidgets.QTableWidget(self.centralwidget)
        self.transaction_table_4.setObjectName("transaction_table_4")
        self.transaction_table_4.setColumnCount(3)
        self.transaction_table_4.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.transaction_table_4.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.transaction_table_4.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.transaction_table_4.setHorizontalHeaderItem(2, item)
        self.gridLayout.addWidget(self.transaction_table_4, 1, 1, 2, 2)
        self.transaction_table_3 = QtWidgets.QTableWidget(self.centralwidget)
        self.transaction_table_3.setMaximumSize(QtCore.QSize(230, 311))
        self.transaction_table_3.setObjectName("transaction_table_3")
        self.transaction_table_3.setColumnCount(1)
        self.transaction_table_3.setRowCount(7)
        item = QtWidgets.QTableWidgetItem()
        self.transaction_table_3.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.transaction_table_3.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.transaction_table_3.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.transaction_table_3.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.transaction_table_3.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.transaction_table_3.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.transaction_table_3.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.transaction_table_3.setHorizontalHeaderItem(0, item)
        self.gridLayout.addWidget(self.transaction_table_3, 2, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 973, 27))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        item = self.transaction_table_1.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "Sale ID"))
        item = self.transaction_table_1.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "Customer ID"))
        item = self.transaction_table_1.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "Customer Name"))
        item = self.transaction_table_1.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Value"))
        item = self.transaction_table_2.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "Date"))
        item = self.transaction_table_2.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "Is Overring?"))
        item = self.transaction_table_2.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Value"))
        item = self.transaction_table_4.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Description"))
        item = self.transaction_table_4.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Unit Cost"))
        item = self.transaction_table_4.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Qty"))
        item = self.transaction_table_3.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "Subtotal"))
        item = self.transaction_table_3.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "Tax"))
        item = self.transaction_table_3.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "Total"))
        item = self.transaction_table_3.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "Cash"))
        item = self.transaction_table_3.verticalHeaderItem(4)
        item.setText(_translate("MainWindow", "Credit"))
        item = self.transaction_table_3.verticalHeaderItem(5)
        item.setText(_translate("MainWindow", "Debit"))
        item = self.transaction_table_3.verticalHeaderItem(6)
        item.setText(_translate("MainWindow", "Misc"))
        item = self.transaction_table_3.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Values"))

