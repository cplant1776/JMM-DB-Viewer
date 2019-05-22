# Standard Library Imports
# Third Party Imports
import sqlite3
# Local Imports

# ==============================================================
# Main
# ==============================================================


class DBCon:
    def __init__(self, db_loc):
        self.conn = sqlite3.connect(db_loc)
        self.cursor = self.conn.cursor()

    def execute_custom_query(self, query=""):
        self.cursor.execute(query)


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