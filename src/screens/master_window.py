# Standard Library Imports
from functools import partial
# Third Party Imports
from PyQt5 import QtCore, QtGui, QtWidgets
# Local Imports
from src.config import SETTINGS
from src.db_con import DBCon
from src.screens.main_window import Ui_MainWindow


class MasterWindow(Ui_MainWindow):
    """
    Extends the Ui_MainWindow class. Exists purely to separate the massive UI definition
    functions (setupUI and retranslateUi) from the UI interaction functions (button bindings, etc)
    """
    def __init__(self):
        super().__init__()
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

    def go_to_item_page(self):
        # Determine result type (customer/layaway/SRO/sale)
        # Populate appropriate page
        # Go to page
        self.go_to_customer_page()
        pass

    def go_to_customer_page(self):
        # Find selected row
        selected_row = self.search_result_table.selectedItems()[0].row()
        # Find customer id on selected row (1st col)
        cust_id = self.search_result_table.item(selected_row, 0).text()
        print("Selected row: {} ==> cust id: {}".format(selected_row, cust_id))
        # Fill in destination page information
        self.populate_customer_page(id=cust_id)
        # Go to destination page
        self.stackedWidget.go_to_screen('customer')

    # ===========================================================================================================
    # CUSTOMER PAGE POPULATION FUNCTIONS
    # ===========================================================================================================
    def populate_customer_page(self, id):
        customer_data = self.db_con.search_by_customer_id(id)[0]
        # Fill in Basic info
        self.fill_customer_page_basic_info_tables(customer_data)
        # Generate potential phone numbers and fill
        self.fill_potential_phone_numbers(customer_data)
        # Fill in notes
        self.notes_tbox.setText(customer_data[SETTINGS['tuple_dicts']['customer']['notes']])
        # Fill in SRO
        self.fill_in_sro(id)
        # Fill in transactions
        self.fill_in_sales(id)
        print("Populated cusotmer page")

    def fill_customer_page_basic_info_tables(self, customer_data):
        # Table 1 - ID/First/Last/Company/Email
        self.customer_table_1.setItem(
            0, 0, QtWidgets.QTableWidgetItem(customer_data[SETTINGS['tuple_dicts']['customer']['customer_id']]))
        self.customer_table_1.setItem(
            0, 1, QtWidgets.QTableWidgetItem(customer_data[SETTINGS['tuple_dicts']['customer']['first_name']]))
        self.customer_table_1.setItem(
            0, 2, QtWidgets.QTableWidgetItem(customer_data[SETTINGS['tuple_dicts']['customer']['last_name']]))
        self.customer_table_1.setItem(
            0, 3, QtWidgets.QTableWidgetItem(customer_data[SETTINGS['tuple_dicts']['customer']['company']]))
        self.customer_table_1.setItem(
            0, 4, QtWidgets.QTableWidgetItem(customer_data[SETTINGS['tuple_dicts']['customer']['email']]))

        # Table 2 - Addr/City/ST/Zip/Last Activity
        self.customer_table_2.setItem(
            0, 0, QtWidgets.QTableWidgetItem(customer_data[SETTINGS['tuple_dicts']['customer']['address']]))
        self.customer_table_2.setItem(
            0, 1, QtWidgets.QTableWidgetItem(customer_data[SETTINGS['tuple_dicts']['customer']['city']]))
        self.customer_table_2.setItem(
            0, 2, QtWidgets.QTableWidgetItem(customer_data[SETTINGS['tuple_dicts']['customer']['state']]))
        self.customer_table_2.setItem(
            0, 3, QtWidgets.QTableWidgetItem(customer_data[SETTINGS['tuple_dicts']['customer']['zip']]))
        self.customer_table_2.setItem(
            0, 4, QtWidgets.QTableWidgetItem(customer_data[SETTINGS['tuple_dicts']['customer']['last_activity']]))

    def fill_potential_phone_numbers(self, customer_data):
        # Generate string to pass
        result = []
        result.append("Home: {}".format(customer_data[SETTINGS['tuple_dicts']['customer']['home_phone']]))
        result.append("Work: {}".format(customer_data[SETTINGS['tuple_dicts']['customer']['work_phone']]))
        result.append("Cell: {}".format(customer_data[SETTINGS['tuple_dicts']['customer']['cell_phone']]))
        numbers_str = "\n".join(result)
        # Fill numbers
        self.phone_tbox.setText(numbers_str)

    def fill_in_sro(self, cust_id):
        orders = self.db_con.sro_search_by_cust_id(cust_id)
        self.sro_table.setRowCount(len(orders))
        for row, r in enumerate(orders):
            self.sro_table.setItem(row, 0,
                                   QtWidgets.QTableWidgetItem(str(r[SETTINGS['tuple_dicts']['sro']['date_in']])))
            self.sro_table.setItem(row, 1,
                                   QtWidgets.QTableWidgetItem(str(r[SETTINGS['tuple_dicts']['sro']['date_complete']])))
            self.sro_table.setItem(row, 2,
                                   QtWidgets.QTableWidgetItem(str(r[SETTINGS['tuple_dicts']['sro']['picked_up']])))
            self.sro_table.setItem(row, 3,
                                   QtWidgets.QTableWidgetItem(str(r[SETTINGS['tuple_dicts']['sro']['make']])))
            self.sro_table.setItem(row, 4,
                                   QtWidgets.QTableWidgetItem(str(r[SETTINGS['tuple_dicts']['sro']['model']])))

    def fill_in_sales(self, cust_id):
        sales = self.db_con.sale_search_by_cust_id(cust_id)
        self.transactions_table.setRowCount(len(sales))
        for row, s in enumerate(sales):
            self.transactions_table.setItem(row, 0,
                                   QtWidgets.QTableWidgetItem(s[SETTINGS['tuple_dicts']['sale']['sale_date']]))
            self.transactions_table.setItem(row, 1,
                                   QtWidgets.QTableWidgetItem(s[SETTINGS['tuple_dicts']['sale']['subtotal']]))
            self.transactions_table.setItem(row, 2,
                                   QtWidgets.QTableWidgetItem(s[SETTINGS['tuple_dicts']['sale']['tax']]))
            self.transactions_table.setItem(row, 3,
                                   QtWidgets.QTableWidgetItem(s[SETTINGS['tuple_dicts']['sale']['total']]))


# ==============================================================
# Main
# ==============================================================
if __name__ == '__main__':
    print("done!")
