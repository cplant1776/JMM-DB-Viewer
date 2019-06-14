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

    # ===========================================================================================================
    # BINDINGS
    # ===========================================================================================================

    def bind_buttons(self):
        # self.search_btn.clicked.connect(partial(self.stackedWidget.go_to_screen, screen='layaway'))
        self.search_btn.clicked.connect(partial(self.stackedWidget.go_to_screen, screen='search'))
        self.serialized_btn.clicked.connect(partial(self.go_to_serialized_inventory))
        self.back_btn_search_result.clicked.connect(partial(self.stackedWidget.go_to_previous_screen))
        self.submit_search_btn.clicked.connect(partial(self.run_search))
        self.back_btn_serial.clicked.connect(partial(self.stackedWidget.go_to_previous_screen))
        self.sro_back_btn.clicked.connect(partial(self.stackedWidget.go_to_previous_screen))
        # self.layaway_btn.clicked.connect(self.run_search)

    def bind_table_behavior(self):
        # Connect double click signal to function
        self.search_result_table.itemDoubleClicked.connect(self.go_to_item_page)
        self.sro_table.itemDoubleClicked.connect(self.go_to_sro_page)
        self.transactions_table.itemDoubleClicked.connect(self.go_to_sale_page)

    # ===========================================================================================================
    # GO TO PAGE X
    # ===========================================================================================================
    def go_to_sro(self, id):
        # populate SRO page
        self.fill_in_sro(id=id)
        # Go to SRO page
        self.stackedWidget.go_to_screen(screen='sro')

    def go_to_sale(self, id):
        # populate sale page
        self.fill_in_sale(id)
        # Go to sale page
        self.stackedWidget.go_to_screen(screen='sale')

    def go_to_customer_page(self):
        # Find selected row
        selected_row = self.search_result_table.selectedItems()[0].row()
        print("selected row: {}".format(selected_row))
        # Find customer id on selected row (1st col)
        cust_id = self.search_result_table.item(selected_row, 0).text()
        print("Selected row: {} ==> cust id: {}".format(selected_row, cust_id))
        # Fill in destination page information
        self.populate_customer_page(id=cust_id)
        # Go to destination page
        self.stackedWidget.go_to_screen('customer')

    def go_to_serialized_inventory(self):
        self.fill_in_serialized_inventory()
        self.serialized_btn.clicked.connect(partial(self.stackedWidget.go_to_screen, screen='serial'))

    def go_to_sro_page(self):
        # Find selected row
        selected_row = self.sro_table.selectedItems()[0].row()
        # Find sro id on selected row (1st col)
        sro_id = self.sro_table.item(selected_row, 5).text()
        print("Selected row: {} ==> SRO id: {}".format(selected_row, sro_id))
        # Fill in destination page information and go to it
        self.go_to_sro(id=sro_id)

    def go_to_sale_page(self):
        # Find selected row
        selected_row = self.transactions_table.selectedItems()[0].row()
        # Find sale id on selected row (1st col)
        sale_id = self.transactions_table.item(selected_row, 4).text()
        print("Selected row: {} ==> sale id: {}".format(selected_row, sale_id))
        # Fill in destination page information and go to it
        self.go_to_sale(id=sale_id)

    # ===========================================================================================================
    # GENERAL FUNCTIONS
    # ===========================================================================================================
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
        self.fill_in_cust_sro(id)
        # Fill in transactions
        self.fill_in_cust_sales(id)
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

    def fill_in_cust_sro(self, cust_id):
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
            self.sro_table.setItem(row, 5,
                                   QtWidgets.QTableWidgetItem(str(r[SETTINGS['tuple_dicts']['sro']['service_id']])))

    def fill_in_cust_sales(self, cust_id):
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
            self.transactions_table.setItem(row, 4,
                                   QtWidgets.QTableWidgetItem(s[SETTINGS['tuple_dicts']['sale']['sale_id']]))

    # ===========================================================================================================
    # SERIALIZED INVENTORY POPULATION FUNCTIONS
    # ===========================================================================================================
    def fill_in_serialized_inventory(self):
        inventory = self.db_con.get_serialized_inventory()
        self.serial_table.setRowCount(len(inventory))
        for row, s in enumerate(inventory):
            self.serial_table.setItem(row, 0,
                                   QtWidgets.QTableWidgetItem(s[SETTINGS['tuple_dicts']['serial']['make']]))
            self.serial_table.setItem(row, 1,
                                   QtWidgets.QTableWidgetItem(s[SETTINGS['tuple_dicts']['serial']['model']]))
            self.serial_table.setItem(row, 2,
                                   QtWidgets.QTableWidgetItem(s[SETTINGS['tuple_dicts']['serial']['serial_num']]))
            self.serial_table.setItem(row, 3,
                                   QtWidgets.QTableWidgetItem(s[SETTINGS['tuple_dicts']['serial']['date_received']]))
            self.serial_table.setItem(row, 4,
                                   QtWidgets.QTableWidgetItem(s[SETTINGS['tuple_dicts']['serial']['notes']]))

    # ===========================================================================================================
    # SRO PAGE POPULATION FUNCTIONS
    # ===========================================================================================================
    def fill_in_sro(self, id):
        sro_data = self.db_con.get_sro_from_id(service_id=id)[0]
        # Fill in basic info
        self.fill_sro_basic_info(data=sro_data)
        # Fill in service request
        self.service_text.setText(sro_data[SETTINGS['tuple_dicts']['sro']['service_request']])
        # Fill in work performed
        self.work_text.setText(sro_data[SETTINGS['tuple_dicts']['sro']['work_performed']])

    def fill_sro_basic_info(self, data):
        self.data_table_3.setItem(0, 0,
                                  QtWidgets.QTableWidgetItem(data[SETTINGS['tuple_dicts']['sro']['service_id']]))
        self.data_table_3.setItem(1, 0,
                                  QtWidgets.QTableWidgetItem(data[SETTINGS['tuple_dicts']['sro']['customer_id']]))
        self.data_table_3.setItem(2, 0,
                                  QtWidgets.QTableWidgetItem(data[SETTINGS['tuple_dicts']['sro']['make']]))
        self.data_table_3.setItem(3, 0,
                                  QtWidgets.QTableWidgetItem(data[SETTINGS['tuple_dicts']['sro']['model']]))
        self.data_table_3.setItem(4, 0,
                                  QtWidgets.QTableWidgetItem(data[SETTINGS['tuple_dicts']['sro']['date_in']]))
        self.data_table_3.setItem(5, 0,
                                  QtWidgets.QTableWidgetItem(data[SETTINGS['tuple_dicts']['sro']['date_complete']]))
        self.data_table_3.setItem(6, 0,
                                  QtWidgets.QTableWidgetItem(data[SETTINGS['tuple_dicts']['sro']['picked_up']]))

    # ===========================================================================================================
    # SALE PAGE POPULATION FUNCTIONS
    # ===========================================================================================================
    def fill_in_sale(self, id):
        sale_data = self.db_con.get_sale_from_id(sale_id=id)[0]
        # Fill in basic info
        self.fill_sale_basic_info(data=sale_data)
        # Fill in line-by-line information
        self.fill_in_sale_items(id)

    def fill_sale_basic_info(self, data):
        # Sale Table 1 - sale id/cust id/cust name
        self.sale_table_1.setItem(0, 0,
                                  QtWidgets.QTableWidgetItem(data[SETTINGS['tuple_dicts']['sale']['sale_id']]))
        self.sale_table_1.setItem(1, 0,
                                  QtWidgets.QTableWidgetItem(data[SETTINGS['tuple_dicts']['sale']['customer_id']]))

        customer_info = self.db_con.search_by_customer_id(id=data[SETTINGS['tuple_dicts']['sale']['customer_id']])[0]
        first_name = customer_info[SETTINGS['tuple_dicts']['customer']['first_name']]
        last_name = customer_info[SETTINGS['tuple_dicts']['customer']['last_name']]
        customer_name = first_name + ' ' + last_name
        self.sale_table_1.setItem(2, 0,
                                  QtWidgets.QTableWidgetItem(customer_name))

        # Sale Table 2 - date/overcharged?
        self.sale_table_2.setItem(0, 0,
                                  QtWidgets.QTableWidgetItem(data[SETTINGS['tuple_dicts']['sale']['sale_date']]))
        self.sale_table_2.setItem(1, 0,
                                  QtWidgets.QTableWidgetItem(data[SETTINGS['tuple_dicts']['sale']['is_overring']]))

        # Sale Table 4 - subtotal/tax/total/cash/credit/debit/misc
        self.sale_table_4.setItem(0, 0,
                                  QtWidgets.QTableWidgetItem(data[SETTINGS['tuple_dicts']['sale']['subtotal']]))
        self.sale_table_4.setItem(1, 0,
                                  QtWidgets.QTableWidgetItem(data[SETTINGS['tuple_dicts']['sale']['tax']]))
        self.sale_table_4.setItem(2, 0,
                                  QtWidgets.QTableWidgetItem(data[SETTINGS['tuple_dicts']['sale']['total']]))
        self.sale_table_4.setItem(3, 0,
                                  QtWidgets.QTableWidgetItem(data[SETTINGS['tuple_dicts']['sale']['cash']]))
        self.sale_table_4.setItem(4, 0,
                                  QtWidgets.QTableWidgetItem(data[SETTINGS['tuple_dicts']['sale']['credit']]))
        self.sale_table_4.setItem(5, 0,
                                  QtWidgets.QTableWidgetItem(data[SETTINGS['tuple_dicts']['sale']['debit']]))
        self.sale_table_4.setItem(6, 0,
                                  QtWidgets.QTableWidgetItem(data[SETTINGS['tuple_dicts']['sale']['misc']]))

    def fill_in_sale_items(self, id):
        sale_items_data = self.db_con.get_sale_items_from_id(sale_id=id)
        self.sale_table_3.setRowCount(len(sale_items_data))
        for row, s in enumerate(sale_items_data):
            self.sale_table_3.setItem(row, 0,
                                   QtWidgets.QTableWidgetItem(str(s[SETTINGS['tuple_dicts']['sale_items']['description']])))
            self.sale_table_3.setItem(row, 1,
                                   QtWidgets.QTableWidgetItem(str(s[SETTINGS['tuple_dicts']['sale_items']['quantity']])))
            self.sale_table_3.setItem(row, 2,
                                   QtWidgets.QTableWidgetItem(str(s[SETTINGS['tuple_dicts']['sale_items']['unit_price']])))
            self.sale_table_3.setItem(row, 3,
                                   QtWidgets.QTableWidgetItem(str(s[SETTINGS['tuple_dicts']['sale_items']['item_discount_perc']])))
            self.sale_table_3.setItem(row, 4,
                                   QtWidgets.QTableWidgetItem(str(s[SETTINGS['tuple_dicts']['sale_items']['item_total']])))


# ==============================================================
# Main
# ==============================================================
if __name__ == '__main__':
    print("done!")
