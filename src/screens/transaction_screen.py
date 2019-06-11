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

        # Create grid layout
        self.sale_grid_layout = QtWidgets.QGridLayout(self.centralwidget)
        self.sale_grid_layout.setObjectName("gridLayout")

        # Sale Table 1 - sale id/cust id/cust name
        self.sale_table_1 = QtWidgets.QTableWidget(self.centralwidget)
        self.sale_table_1.setMaximumSize(QtCore.QSize(261, 151))
        self.sale_table_1.setObjectName("sale_table_1")
        self.sale_table_1.setColumnCount(1)
        self.sale_table_1.setRowCount(3)
        item = QtWidgets.QTableWidgetItem()
        self.sale_table_1.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.sale_table_1.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.sale_table_1.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.sale_table_1.setHorizontalHeaderItem(0, item)
        self.sale_grid_layout.addWidget(self.sale_table_1, 0, 0, 1, 1)

        # Spacer
        spacerItem = QtWidgets.QSpacerItem(442, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.sale_grid_layout.addItem(spacerItem, 0, 1, 1, 1)

        # Sale Table 2 - date/overcharged?
        self.sale_table_2 = QtWidgets.QTableWidget(self.centralwidget)
        self.sale_table_2.setMaximumSize(QtCore.QSize(231, 111))
        self.sale_table_2.setObjectName("sale_table_2")
        self.sale_table_2.setColumnCount(1)
        self.sale_table_2.setRowCount(2)
        item = QtWidgets.QTableWidgetItem()
        self.sale_table_2.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.sale_table_2.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.sale_table_2.setHorizontalHeaderItem(0, item)
        self.sale_grid_layout.addWidget(self.sale_table_2, 0, 2, 1, 1)

        # Spacer
        spacerItem1 = QtWidgets.QSpacerItem(20, 278, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.sale_grid_layout.addItem(spacerItem1, 1, 0, 1, 1)

        # Sale Table 3 - desc/unit cost/qty
        self.sale_table_3 = QtWidgets.QTableWidget(self.centralwidget)
        self.sale_table_3.setObjectName("sale_table_3")
        self.sale_table_3.setColumnCount(3)
        self.sale_table_3.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.sale_table_3.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.sale_table_3.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.sale_table_3.setHorizontalHeaderItem(2, item)
        self.sale_grid_layout.addWidget(self.sale_table_3, 1, 1, 2, 2)

        # Sale Table 4 - subtotal/tax/total/cash/credit/debit/misc
        self.sale_table_4 = QtWidgets.QTableWidget(self.centralwidget)
        self.sale_table_4.setMaximumSize(QtCore.QSize(230, 311))
        self.sale_table_4.setObjectName("sale_table_4")
        self.sale_table_4.setColumnCount(1)
        self.sale_table_4.setRowCount(7)
        item = QtWidgets.QTableWidgetItem()
        self.sale_table_4.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.sale_table_4.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.sale_table_4.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.sale_table_4.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.sale_table_4.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.sale_table_4.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.sale_table_4.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.sale_table_4.setHorizontalHeaderItem(0, item)
        self.sale_grid_layout.addWidget(self.sale_table_4, 2, 0, 1, 1)


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
        item = self.sale_table_1.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "Sale ID"))
        item = self.sale_table_1.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "Customer ID"))
        item = self.sale_table_1.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "Customer Name"))
        item = self.sale_table_1.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Value"))
        item = self.sale_table_2.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "Date"))
        item = self.sale_table_2.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "Is Overring?"))
        item = self.sale_table_2.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Value"))
        item = self.sale_table_3.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Description"))
        item = self.sale_table_3.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Unit Cost"))
        item = self.sale_table_3.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Qty"))
        item = self.sale_table_4.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "Subtotal"))
        item = self.sale_table_4.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "Tax"))
        item = self.sale_table_4.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "Total"))
        item = self.sale_table_4.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "Cash"))
        item = self.sale_table_4.verticalHeaderItem(4)
        item.setText(_translate("MainWindow", "Credit"))
        item = self.sale_table_4.verticalHeaderItem(5)
        item.setText(_translate("MainWindow", "Debit"))
        item = self.sale_table_4.verticalHeaderItem(6)
        item.setText(_translate("MainWindow", "Misc"))
        item = self.sale_table_4.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Values"))


