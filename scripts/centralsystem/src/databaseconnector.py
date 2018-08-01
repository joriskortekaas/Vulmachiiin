import MySQLdb
import math
import methods

class DatabaseConnector():
    '''Class used for connecting with the database. Connecting without this class is heavily discouraged.

       NOTE THAT THIS IS JUST FOR OUR DATABASE DONT USE ON OTHER DATABASES'''

    def __init__(self):
        self.db = self.setup_connection()
        self.db.autocommit(True)
        print('connected to the database')

    def __del__(self):
        self.db.close()

    def setup_connection(self):
        return MySQLdb.connect(host='localhost',
                               user='vulmachiiin',
                               passwd='V0etInM0nd!',
                               db='vulmachiiin')

    def get_query(self, query):
        cursor = self.db.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return results

    def execute_query(self, query):
        cursor = self.db.cursor()
        cursor.execute(query)
        self.db.commit()

if __name__ == '__main__':
    db = DatabaseConnector()
    print(db.get_query('SELECT * FROM productsinshelve'))
