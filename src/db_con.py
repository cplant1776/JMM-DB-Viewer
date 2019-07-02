# Standard Library Imports
import re
# Third Party Imports
import sqlite3
# Local Imports
from src.config import SETTINGS

# ==============================================================
# Main
# ==============================================================


class DBCon:
    def __init__(self, db_loc):
        self.conn = sqlite3.connect(db_loc)
        self.cursor = self.conn.cursor()
        self.general_search_results = []

    # ===========================================================================================================
    # GENERAL FUNCTIONS
    # ===========================================================================================================
    def execute_custom_query(self, query=""):
        self.cursor.execute(query)

    def fetch_cursor(self):
        return self.cursor.fetchall()

    @staticmethod
    def extract_phone_number(num=""):
        raw_num = re.sub('[^\d]', '', num)
        if len(raw_num) < 10:
            print("Invalid phone number - too short: {}".format(raw_num))
            return "0" * 10
        else:
            return raw_num

    # ===========================================================================================================
    # SEARCH CUSTOMER BY X
    # ===========================================================================================================
    def search_by_number(self, number):
        number = self.extract_phone_number(number)
        self.cursor.execute('''
        SELECT *
        FROM customer
        WHERE
        cell_phone LIKE ?
        OR home_phone LIKE ?
        OR work_phone LIKE ?
        ''', ('%'+number+'%', '%'+number+'%', '%'+number+'%'))
        return self.fetch_cursor()

    def search_by_first_name(self, name):
        name = name.upper()
        self.cursor.execute('''
        SELECT *
        FROM customer
        WHERE first_name
        LIKE ?
        ''', ('%'+name.upper()+'%',))
        return self.fetch_cursor()

    def search_by_last_name(self, name):
        name = name.upper()
        self.cursor.execute('''
        SELECT *
        FROM customer
        WHERE last_name
        LIKE ?
        ''', ('%'+name.upper()+'%',))
        return self.fetch_cursor()

    def search_by_customer_id(self, id):
        self.cursor.execute('''
        SELECT *
        FROM customer
        WHERE customer_id=?
        ''', (id,))
        return self.fetch_cursor()

    # ===========================================================================================================
    # SEARCH X BY CUSTOMER ID
    # ===========================================================================================================
    def sro_search_by_cust_id(self, id):
        self.cursor.execute('''
        SELECT *
        FROM service
        WHERE customer_id=?
        ''', (id,))
        return self.fetch_cursor()

    def sale_search_by_cust_id(self, id):
        self.cursor.execute('''
        SELECT *
        FROM sale
        WHERE customer_id=?
        ''', (id,))
        return self.fetch_cursor()

    def layaway_search_by_cust_id(self, id):
        self.cursor.execute('''
        SELECT *
        FROM layaway
        WHERE customer_id=?
        ''', (id,))
        return self.fetch_cursor()

    # ===========================================================================================================
    # SERIALIZED INVENTORY SEARCH
    # ===========================================================================================================
    def get_serialized_inventory(self):
        self.cursor.execute('''
        SELECT *
        FROM serialized_inv
        ''')
        return self.fetch_cursor()

    # ===========================================================================================================
    # SEARCH X BY SERVICE ID
    # ===========================================================================================================
    def get_sro_from_id(self, service_id):
        self.cursor.execute('''
        SELECT *
        FROM service
        WHERE service_id=?
        ''', (service_id,))
        return self.fetch_cursor()

    # ===========================================================================================================
    # SEARCH X BY SALE ID
    # ===========================================================================================================
    def get_sale_from_id(self, sale_id):
        self.cursor.execute('''
        SELECT *
        FROM sale
        WHERE sale_id=?
        ''', (sale_id,))
        return self.fetch_cursor()

    def get_sale_items_from_id(self, sale_id):
        self.cursor.execute('''
        SELECT *
        FROM sale_items
        WHERE sale_id=?
        ''', (sale_id,))
        return self.fetch_cursor()

    # ===========================================================================================================
    # SEARCH X BY LAYAWAY ID
    # ===========================================================================================================
    def get_layaway_from_id(self, layaway_id):
        self.cursor.execute('''
        SELECT *
        FROM layaway
        WHERE layaway_id=?
        ''', (layaway_id,))
        return self.fetch_cursor()

    # ===========================================================================================================
    # GENERAL SEARCH FUNCTIONS - Unimplemented. Not worth time.
    # ===========================================================================================================
    def run_general_query(self, query, query_type, term):
        print("Executing: {}".format(query))
        self.cursor.execute(query, term)
        result = self.fetch_cursor()
        if result:
            self.general_search_results.append(GeneralResult(result=result, query_type=query_type))

    def general_search(self, term):
        self.general_search_results = []
        for query_type, queries in SETTINGS['general_search_query'].items():
            if isinstance(queries, str):
                self.run_general_query(queries, query_type, term)
            else:
                for query in queries:
                    self.run_general_query(query, query_type, term)
        return self.general_search_results


class GeneralResult:
    def __init__(self, result, query_type):
        self.result = result
        self.query_type = query_type

    def get_result(self):
        return self.result

    def get_query_type(self):
        return self.query_type
