import mysql.connector as con

class Database:
    def __init__(self):
        try:
            self.connection = con.connect(
                user = 'root',
                host = 'localhost',
                database = 'test1',
                passwd = 'r00tP45s!'
            )
            self.cur = self.connection.cursor()
        except con.Error as err:
            print(f"Error: {err}\nTry again later!")
            self.connection = None


    def close(self):
        if self.cur:
            self.cur.close()
        if self.connection:
            self.connection.close()
