# Standard Library Imports
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

    def execute_custom_query(self, query=""):
        self.cursor.execute(query)

    def fetch_cursor(self):
        return self.cursor.fetchall()

    def search_by_number(self, number):
        self.cursor.execute('''
        SELECT *
        FROM customer
        WHERE cell_phone=? OR home_phone=? OR work_phone=?
        ''', (number, number, number))
        return self.fetch_cursor()

    def search_by_first_name(self, name):
        self.cursor.execute('''
        SELECT *
        FROM customer
        WHERE first_name=?
        ''', (name,))
        return self.fetch_cursor()

    def search_by_last_name(self, name):
        self.cursor.execute('''
        SELECT *
        FROM customer
        WHERE last_name=?
        ''', (name,))
        return self.fetch_cursor()

    def search_by_customer_id(self, id):
        self.cursor.execute('''
        SELECT *
        FROM customer
        WHERE customer_id=?
        ''', (id,))
        return self.fetch_cursor()

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



# # Never do this -- insecure!
# symbol = 'RHAT'
# c.execute("SELECT * FROM stocks WHERE symbol = '%s'" % symbol)
#
# # Do this instead
# t = ('RHAT',)
# c.execute('SELECT * FROM stocks WHERE symbol=?', t)
# print(c.fetchone())
#
# # Larger example that inserts many records at a time
# purchases = [('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
#              ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
#              ('2006-04-06', 'SELL', 'IBM', 500, 53.00),
#             ]
# c.executemany('INSERT INTO stocks VALUES (?,?,?,?,?)', purchases)