# Standard Library Imports
from functools import partial
from datetime import datetime
# Third Party Imports
from PyQt5 import QtCore, QtGui, QtWidgets
# Local Imports
from src.config import SETTINGS
from src.db_con import DBCon
from src.screens.main_window import Ui_MainWindow
from src.screens.screen_functions.stacked_widget_subclass import MyStackWidget


class MasterWindow(Ui_MainWindow):
    """
    Extends the Ui_MainWindow class. Exists purely to separate the massive UI definition
    functions (setupUI and retranslateUi) from the UI interaction functions (button bindings, etc)
    """

    def __init__(self):
        super().__init__()
        # Add database connection
        self.db_con = DBCon(db_loc=SETTINGS['local_database_path'])
        # List of references to tables with dynamic behavior
        self.dynamic_tables = []

    # ===========================================================================================================
    # BUTTON BINDINGS
    # ===========================================================================================================
    def bind_buttons(self):
        # self.search_btn.clicked.connect(partial(self.go_to_layaway, id=76))
        self.search_btn.clicked.connect(partial(self.stackedWidget.go_to_screen, screen='search'))
        self.serialized_btn.clicked.connect(partial(self.stackedWidget.go_to_screen, screen='serial'))
        self.submit_search_btn.clicked.connect(partial(self.run_search))

        # Back buttons
        self.back_btn_search_result.clicked.connect(partial(self.stackedWidget.go_to_screen, screen='search'))
        self.back_btn_serial.clicked.connect(partial(self.stackedWidget.go_to_previous_screen))
        self.sro_back_btn.clicked.connect(partial(self.stackedWidget.go_to_previous_screen))
        self.back_btn_sale.clicked.connect(partial(self.stackedWidget.go_to_previous_screen))
        self.back_btn_customer.clicked.connect(partial(self.stackedWidget.go_to_screen, screen='search_result'))
        self.back_btn_search.clicked.connect(partial(self.stackedWidget.go_to_screen, screen='start'))
        self.back_btn_layaway.clicked.connect(partial(self.stackedWidget.go_to_previous_screen))

    # ===========================================================================================================
    # LINE EDIT BINDINGS
    # ===========================================================================================================
    def bind_line_edits(self):
        self.first_search.returnPressed.connect(partial(self.run_first_name_search))
        self.last_search.returnPressed.connect(partial(self.run_last_name_search))
        self.phone_search.returnPressed.connect(partial(self.run_phone_search))

    # ===========================================================================================================
    # TABLE BINDINGS
    # ===========================================================================================================
    def bind_table_behavior(self):
        # Connect double click signal to function
        self.search_result_table.itemDoubleClicked.connect(self.go_to_item_page)
        self.sro_table.itemDoubleClicked.connect(self.go_to_sro_page)
        self.transactions_table.itemDoubleClicked.connect(self.go_to_sale_page)
        self.layaways_table.itemDoubleClicked.connect(self.go_to_layaway_page)

        # List of references to tables with dynamic behavior
        self.dynamic_tables = [self.sale_lines_table,
                               self.layaways_table,
                               self.transactions_table,
                               self.sro_table,
                               self.serial_table,
                               self.search_result_table]
        # Connect table header click signal to function
        self.connect_table_header_behavior()

    def connect_table_header_behavior(self):
        for table in self.dynamic_tables:
            # Initialize table sort order
            table.sort_ascending = False
            # Connect sort function to clicking header of column
            table.horizontalHeader().sectionClicked.connect(partial(self.sort_table_by_col,
                                                                    table))

    @staticmethod
    def sort_table_by_col(table):
        try:
            # Get the selected column
            selected_column = table.selectedItems()[0].column()
        except IndexError:
            return
        # Sort table by selected column. If already ascending, descend. If already descending, ascend.
        if table.sort_ascending:
            table.sortByColumn(selected_column, QtCore.Qt.AscendingOrder)
            table.sort_ascending = False
            print('Sorting ascending.')
        else:
            table.sortByColumn(selected_column, QtCore.Qt.DescendingOrder)
            table.sort_ascending = True
            print('Sorting descending.')

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

    def go_to_layaway(self, id):
        # populate layaway page
        self.fill_in_layaway(id)
        # Go to sale page
        self.stackedWidget.go_to_screen(screen='layaway')

    def go_to_customer_page(self):
        try:
            # Find selected row
            selected_row = self.search_result_table.selectedItems()[0].row()
        except IndexError:
            return
        print("selected row: {}".format(selected_row))
        # Find customer id on selected row (1st col)
        cust_id = self.search_result_table.item(selected_row, 0).text()
        print("Selected row: {} ==> cust id: {}".format(selected_row, cust_id))
        # Fill in destination page information
        self.populate_customer_page(id=cust_id)
        # Go to destination page
        self.stackedWidget.go_to_screen('customer')

    def go_to_sro_page(self):
        try:
            # Find selected row
            selected_row = self.sro_table.selectedItems()[0].row()
        except IndexError:
            return
        # Find sro id on selected row (1st col)
        sro_id = self.sro_table.item(selected_row, 5).text()
        print("Selected row: {} ==> SRO id: {}".format(selected_row, sro_id))
        # Fill in destination page information and go to it
        self.go_to_sro(id=sro_id)

    def go_to_sale_page(self):
        try:
            # Find selected row
            selected_row = self.transactions_table.selectedItems()[0].row()
        except IndexError:
            return
        # Find sale id on selected row (1st col)
        sale_id = self.transactions_table.item(selected_row, 4).text()
        print("Selected row: {} ==> sale id: {}".format(selected_row, sale_id))
        # Fill in destination page information and go to it
        self.go_to_sale(id=sale_id)

    def go_to_layaway_page(self):
        try:
            # Find selected row
            selected_row = self.layaways_table.selectedItems()[0].row()
        except IndexError:
            return
        # Find sale id on selected row (1st col)
        layaway_id = self.layaways_table.item(selected_row, 2).text()
        print("Selected row: {} ==> layaway id: {}".format(selected_row, layaway_id))
        # Fill in destination page information and go to it
        self.go_to_layaway(id=layaway_id)

    # ===========================================================================================================
    # SEARCH FUNCTIONS
    # ===========================================================================================================
    def run_search(self):
        # Run appropriate query and store result
        if self.first_radio.isChecked():
            self.run_first_name_search()
        elif self.last_radio.isChecked():
            self.run_last_name_search()
        elif self.phone_radio.isChecked():
            self.run_phone_search()
        else:
            return

    def run_first_name_search(self):
        first = self.first_search.text()
        if first != '':
            print("First name search: {}".format(first))
            result = self.db_con.search_by_first_name(first)
            self.populate_search_result(result=result)
            self.stackedWidget.go_to_screen(screen='search_result')

    def run_last_name_search(self):
        last = self.last_search.text()
        if last != '':
            print("Last name search: {}".format(last))
            result = self.db_con.search_by_last_name(last)
            self.populate_search_result(result=result)
            self.stackedWidget.go_to_screen(screen='search_result')

    def run_phone_search(self):
        num = self.phone_search.text()
        if num != '':
            print("Phone search: {}".format(num))
            result = self.db_con.search_by_number(num)
            self.populate_search_result(result=result)
            self.stackedWidget.go_to_screen(screen='search_result')

    # ===========================================================================================================
    # GENERAL FUNCTIONS
    # ===========================================================================================================
    def populate_search_result(self, result):
        self.search_result_table.setRowCount(len(result))
        for row, r in enumerate(result):
            try:
                item = MyTableWidgetItem(str(r[SETTINGS['tuple_dicts']['customer']['customer_id']]),
                                         sort_key=int(r[SETTINGS['tuple_dicts']['customer']['customer_id']]))
                self.search_result_table.setItem(row, 0, item)
            except TypeError:
                pass
            try:
                item = MyTableWidgetItem(str(r[SETTINGS['tuple_dicts']['customer']['first_name']]))
                self.search_result_table.setItem(row, 1, item)
            except TypeError:
                pass
            try:
                item = MyTableWidgetItem(str(r[SETTINGS['tuple_dicts']['customer']['last_name']]))
                self.search_result_table.setItem(row, 2, item)
            except TypeError:
                pass
            try:
                item = MyTableWidgetItem(str(r[SETTINGS['tuple_dicts']['customer']['address']]))
                self.search_result_table.setItem(row, 3, item)
            except TypeError:
                pass
            try:
                item = MyTableWidgetItem(str(r[SETTINGS['tuple_dicts']['customer']['city']]))
                self.search_result_table.setItem(row, 4, item)
            except TypeError:
                pass
            try:
                item = MyTableWidgetItem(str(r[SETTINGS['tuple_dicts']['customer']['state']]))
                self.search_result_table.setItem(row, 5, item)
            except TypeError:
                pass
            try:
                item = MyTableWidgetItem(str(r[SETTINGS['tuple_dicts']['customer']['zip']]))
                self.search_result_table.setItem(row, 6, item)
            except TypeError:
                pass
            try:
                item = MyTableWidgetItem(str(r[SETTINGS['tuple_dicts']['customer']['home_phone']]))
                self.search_result_table.setItem(row, 7, item)
            except TypeError:
                pass
            try:
                item = MyTableWidgetItem(str(r[SETTINGS['tuple_dicts']['customer']['work_phone']]))
                self.search_result_table.setItem(row, 8, item)
            except TypeError:
                pass
            try:
                item = MyTableWidgetItem(str(r[SETTINGS['tuple_dicts']['customer']['cell_phone']]))
                self.search_result_table.setItem(row, 9, item)
            except TypeError:
                pass

            try:
                item = MyTableWidgetItem(str(r[SETTINGS['tuple_dicts']['customer']['added']]),
                                         sort_key=datetime.strptime(r[SETTINGS['tuple_dicts']['customer']['added']],
                                         "%m/%d/%Y"))
                self.search_result_table.setItem(row, 10, item)
            except TypeError:
                pass

            try:
                item = MyTableWidgetItem(str(r[SETTINGS['tuple_dicts']['customer']['last_activity']]),
                                         sort_key=datetime.strptime(r[SETTINGS['tuple_dicts']['customer']['last_activity']],
                                                                    "%m/%d/%Y"))
                self.search_result_table.setItem(row, 11, item)
            except TypeError:
                pass

        # for row, r in enumerate(result):
        #     for col, item in enumerate(r):
        #         self.search_result_table.setItem(row, col, QtWidgets.QTableWidgetItem(item))
        self.search_result_table.resizeColumnsToContents()

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
        # Fill in layaways
        self.fill_in_cust_layaways(id)
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
            try:
                item = MyTableWidgetItem(str(r[SETTINGS['tuple_dicts']['sro']['date_in']]),
                                         sort_key=datetime.strptime(r[SETTINGS['tuple_dicts']['sro']['date_in']],
                                         "%m/%d/%Y"))
                self.sro_table.setItem(row, 0, item)
            except TypeError:
                pass

            try:
                item = MyTableWidgetItem(str(r[SETTINGS['tuple_dicts']['sro']['date_complete']]),
                                         sort_key=datetime.strptime(r[SETTINGS['tuple_dicts']['sro']['date_complete']],
                                                                    "%m/%d/%Y"))
                self.sro_table.setItem(row, 1, item)
            except TypeError:
                pass

            try:
                item = MyTableWidgetItem(str(r[SETTINGS['tuple_dicts']['sro']['picked_up']]),
                                         sort_key=datetime.strptime(r[SETTINGS['tuple_dicts']['sro']['picked_up']],
                                         "%m/%d/%Y"))
                self.sro_table.setItem(row, 2, item)
            except TypeError:
                pass

            item = MyTableWidgetItem(str(r[SETTINGS['tuple_dicts']['sro']['make']]))
            self.sro_table.setItem(row, 3, item)
            item = MyTableWidgetItem(str(r[SETTINGS['tuple_dicts']['sro']['model']]))
            self.sro_table.setItem(row, 4, item)
            item = MyTableWidgetItem(str(r[SETTINGS['tuple_dicts']['sro']['service_id']]),
                                     sort_key=int(r[SETTINGS['tuple_dicts']['sro']['service_id']]))
            self.sro_table.setItem(row, 5, item)


    def fill_in_cust_sales(self, cust_id):
        sales = self.db_con.sale_search_by_cust_id(cust_id)
        self.transactions_table.setRowCount(len(sales))
        for row, s in enumerate(sales):

            try:
                item = MyTableWidgetItem(str(s[SETTINGS['tuple_dicts']['sale']['sale_date']]),
                                         sort_key=datetime.strptime(s[SETTINGS['tuple_dicts']['sale']['sale_date']],
                                                                    "%m/%d/%Y"))
                self.transactions_table.setItem(row, 0, item)
            except TypeError:
                pass

            item = MyTableWidgetItem(str(s[SETTINGS['tuple_dicts']['sale']['subtotal']]),
                                     sort_key=float(s[SETTINGS['tuple_dicts']['sale']['subtotal']]))
            self.transactions_table.setItem(row, 1, item)
            item = MyTableWidgetItem(str(s[SETTINGS['tuple_dicts']['sale']['tax']]),
                                     sort_key=float(s[SETTINGS['tuple_dicts']['sale']['tax']]))
            self.transactions_table.setItem(row, 2, item)
            item = MyTableWidgetItem(str(s[SETTINGS['tuple_dicts']['sale']['total']]),
                                     sort_key=float(s[SETTINGS['tuple_dicts']['sale']['total']]))
            self.transactions_table.setItem(row, 3, item)
            item = MyTableWidgetItem(str(s[SETTINGS['tuple_dicts']['sale']['sale_id']]),
                                     sort_key=int(s[SETTINGS['tuple_dicts']['sale']['sale_id']]))
            self.transactions_table.setItem(row, 4, item)

    def fill_in_cust_layaways(self, cust_id):
        layaways = self.db_con.layaway_search_by_cust_id(cust_id)
        self.layaways_table.setRowCount(len(layaways))
        for row, s in enumerate(layaways):
            try:
                item = MyTableWidgetItem(str(s[SETTINGS['tuple_dicts']['layaway']['start_date']]),
                                         sort_key=datetime.strptime(s[SETTINGS['tuple_dicts']['layaway']['start_date']],
                                                                    "%m/%d/%Y"))
                self.layaways_table.setItem(row, 0, item)
            except TypeError:
                pass
            try:

                item = MyTableWidgetItem(str(s[SETTINGS['tuple_dicts']['layaway']['balance_due']]),
                                         sort_key=float(s[SETTINGS['tuple_dicts']['layaway']['balance_due']]))
                self.layaways_table.setItem(row, 1, item)
            except TypeError:
                pass
            try:
                item = MyTableWidgetItem(str(s[SETTINGS['tuple_dicts']['layaway']['layaway_id']]),
                                         sort_key=int(s[SETTINGS['tuple_dicts']['layaway']['layaway_id']]))
                self.layaways_table.setItem(row, 2, item)
            except TypeError:
                pass

    # ===========================================================================================================
    # SERIALIZED INVENTORY POPULATION FUNCTIONS
    # ===========================================================================================================
    def fill_in_serialized_inventory(self):
        inventory = self.db_con.get_serialized_inventory()
        self.serial_table.setRowCount(len(inventory))
        for row, s in enumerate(inventory):
            item = MyTableWidgetItem(s[SETTINGS['tuple_dicts']['serial']['make']])
            self.serial_table.setItem(row, 0, item)
            item = MyTableWidgetItem(s[SETTINGS['tuple_dicts']['serial']['model']])
            self.serial_table.setItem(row, 1, item)
            item = MyTableWidgetItem(s[SETTINGS['tuple_dicts']['serial']['serial_num']])
            self.serial_table.setItem(row, 2, item)
            # Pass if date empty
            try:
                item = MyTableWidgetItem(s[SETTINGS['tuple_dicts']['serial']['date_received']],
                                         sort_key=datetime.strptime(s[SETTINGS['tuple_dicts']['serial']['date_received']],
                                         "%m/%d/%Y"))
                # print("{} | {}".format(item.text, item.sort_key))
                self.serial_table.setItem(row, 3, item)
            except TypeError:
                pass

            item = MyTableWidgetItem(s[SETTINGS['tuple_dicts']['serial']['notes']])
            self.serial_table.setItem(row, 4, item)
        self.serial_table.resizeColumnsToContents()

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
        self.sro_basic_table.setItem(0, 0,
                                  QtWidgets.QTableWidgetItem(data[SETTINGS['tuple_dicts']['sro']['service_id']]))
        self.sro_basic_table.setItem(1, 0,
                                  QtWidgets.QTableWidgetItem(data[SETTINGS['tuple_dicts']['sro']['customer_id']]))
        self.sro_basic_table.setItem(2, 0,
                                  QtWidgets.QTableWidgetItem(data[SETTINGS['tuple_dicts']['sro']['make']]))
        self.sro_basic_table.setItem(3, 0,
                                  QtWidgets.QTableWidgetItem(data[SETTINGS['tuple_dicts']['sro']['model']]))
        self.sro_basic_table.setItem(4, 0,
                                  QtWidgets.QTableWidgetItem(data[SETTINGS['tuple_dicts']['sro']['date_in']]))
        self.sro_basic_table.setItem(5, 0,
                                  QtWidgets.QTableWidgetItem(data[SETTINGS['tuple_dicts']['sro']['date_complete']]))
        self.sro_basic_table.setItem(6, 0,
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
        # Sale basic info table - sale id/cust id/cust name/date/overcharged
        self.sale_basic_info.setItem(0, 0,
                                  QtWidgets.QTableWidgetItem(data[SETTINGS['tuple_dicts']['sale']['sale_id']]))
        self.sale_basic_info.setItem(1, 0,
                                  QtWidgets.QTableWidgetItem(data[SETTINGS['tuple_dicts']['sale']['customer_id']]))

        # Create customer name
        customer_info = self.db_con.search_by_customer_id(id=data[SETTINGS['tuple_dicts']['sale']['customer_id']])[0]
        first_name = customer_info[SETTINGS['tuple_dicts']['customer']['first_name']]
        last_name = customer_info[SETTINGS['tuple_dicts']['customer']['last_name']]
        customer_name = first_name + ' ' + last_name

        self.sale_basic_info.setItem(2, 0,
                                  QtWidgets.QTableWidgetItem(customer_name))
        self.sale_basic_info.setItem(3, 0,
                                  QtWidgets.QTableWidgetItem(data[SETTINGS['tuple_dicts']['sale']['sale_date']]))
        self.sale_basic_info.setItem(4, 0,
                                  QtWidgets.QTableWidgetItem(data[SETTINGS['tuple_dicts']['sale']['is_overring']]))

        # Sale Totals - subtotal/tax/total/cash/credit/debit/misc
        self.sale_totals.setItem(0, 0,
                                  QtWidgets.QTableWidgetItem(data[SETTINGS['tuple_dicts']['sale']['subtotal']]))
        self.sale_totals.setItem(1, 0,
                                  QtWidgets.QTableWidgetItem(data[SETTINGS['tuple_dicts']['sale']['tax']]))
        self.sale_totals.setItem(2, 0,
                                  QtWidgets.QTableWidgetItem(data[SETTINGS['tuple_dicts']['sale']['total']]))
        self.sale_totals.setItem(3, 0,
                                  QtWidgets.QTableWidgetItem(data[SETTINGS['tuple_dicts']['sale']['cash']]))
        self.sale_totals.setItem(4, 0,
                                  QtWidgets.QTableWidgetItem(data[SETTINGS['tuple_dicts']['sale']['credit']]))
        self.sale_totals.setItem(5, 0,
                                  QtWidgets.QTableWidgetItem(data[SETTINGS['tuple_dicts']['sale']['debit']]))
        self.sale_totals.setItem(6, 0,
                                  QtWidgets.QTableWidgetItem(data[SETTINGS['tuple_dicts']['sale']['misc']]))

    def fill_in_sale_items(self, id):
        sale_items_data = self.db_con.get_sale_items_from_id(sale_id=id)
        self.sale_lines_table.setRowCount(len(sale_items_data))
        for row, s in enumerate(sale_items_data):
            try:
                item = MyTableWidgetItem(str(s[SETTINGS['tuple_dicts']['sale_items']['quantity']]),
                                         sort_key=int(s[SETTINGS['tuple_dicts']['sale_items']['quantity']]))
                self.sale_lines_table.setItem(row, 0, item)
            except TypeError:
                pass
            try:
                item = MyTableWidgetItem(str(s[SETTINGS['tuple_dicts']['sale_items']['unit_price']]),
                                         sort_key=float(s[SETTINGS['tuple_dicts']['sale_items']['unit_price']]))
                self.sale_lines_table.setItem(row, 1, item)
            except TypeError:
                pass
            try:
                item = MyTableWidgetItem(str(s[SETTINGS['tuple_dicts']['sale_items']['item_discount_perc']]),
                                         sort_key=float(s[SETTINGS['tuple_dicts']['sale_items']['item_discount_perc']]))
                self.sale_lines_table.setItem(row, 2, item)
            except TypeError:
                pass
            try:
                item = MyTableWidgetItem(str(s[SETTINGS['tuple_dicts']['sale_items']['item_total']]),
                                         sort_key=float(s[SETTINGS['tuple_dicts']['sale_items']['item_total']]))
                self.sale_lines_table.setItem(row, 3, item)
            except TypeError:
                pass
            try:
                item = MyTableWidgetItem(s[SETTINGS['tuple_dicts']['sale_items']['description']])
                self.sale_lines_table.setItem(row, 4, item)
            except TypeError:
                pass
    # ===========================================================================================================
    # LAYAWAY PAGE POPULATION FUNCTIONS
    # ===========================================================================================================
    def fill_in_layaway(self, id):
        layaway_data = self.db_con.get_layaway_from_id(layaway_id=id)[0]
        # Fill in basic info
        self.fill_layaway_basic_info(data=layaway_data)
        # Fill in notes
        self.fill_layaway_notes(data=layaway_data)
        # Fill in transaction history
        self.fill_transaction_history(data=layaway_data)

    def fill_layaway_basic_info(self, data):
        # Layaway Table 1 - layaway id/customer id/name/start
        self.layaway_table_1.setItem(0, 0,
                                  QtWidgets.QTableWidgetItem(data[SETTINGS['tuple_dicts']['layaway']['layaway_id']]))
        self.layaway_table_1.setItem(1, 0,
                                  QtWidgets.QTableWidgetItem(data[SETTINGS['tuple_dicts']['layaway']['customer_id']]))
        self.layaway_table_1.setItem(2, 0,
                                  QtWidgets.QTableWidgetItem(data[SETTINGS['tuple_dicts']['layaway']['cust_name']]))
        # Layaway Table 2 - start date/pay recvd/balance due
        self.layaway_table_2.setItem(0, 0,
                                  QtWidgets.QTableWidgetItem(data[SETTINGS['tuple_dicts']['layaway']['start_date']]))
        self.layaway_table_2.setItem(1, 0,
                                  QtWidgets.QTableWidgetItem(data[SETTINGS['tuple_dicts']['layaway']['payments_received']]))
        self.layaway_table_2.setItem(2, 0,
                                  QtWidgets.QTableWidgetItem(data[SETTINGS['tuple_dicts']['layaway']['balance_due']]))

    def fill_layaway_notes(self, data):
        # Fill initial notes
        self.layaway_initial_notes_tbox.setText(data[SETTINGS['tuple_dicts']['layaway']['initial_notes']])
        # Fill notes
        self.layaway_notes_tbox.setText(data[SETTINGS['tuple_dicts']['layaway']['notes']])

    def fill_transaction_history(self, data):
        self.layaway_transaction_history_tbox.setText(data[SETTINGS['tuple_dicts']['layaway']['transaction_history']])


# ==============================================================
# Override Default QTableWidgetItem
# ==============================================================
class MyTableWidgetItem(QtWidgets.QTableWidgetItem):
    """Adds a sort key argument to QTableWidgetItem so items can be sorted by non-displayed attribute"""
    def __init__(self, text, sort_key=None):
            QtWidgets.QTableWidgetItem.__init__(self, text, QtWidgets.QTableWidgetItem.UserType)
            if sort_key:
                self.sort_key = sort_key
            else:
                self.sort_key = str(text)

    def __lt__(self, other):
        """Override default less than method"""
        if self.sort_key == '0' or self.sort_key == '0.0' or self.sort_key == 0:
            self.sort_key = float(0)
        if other.sort_key == '0' or other.sort_key == '0.0' or other.sort_key == 0:
            other.sort_key = float(0)
        print("{}, {} | {}, {}".format(self.sort_key, type(self.sort_key), other.sort_key, type(other.sort_key)))
        return self.sort_key < other.sort_key


# ==============================================================
# Main
# ==============================================================
if __name__ == '__main__':
    print("done!")
