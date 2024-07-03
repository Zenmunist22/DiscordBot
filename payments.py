import mysql.connector as con
import users
import datetime
#CREATE TABLE payments (id INT PRIMARY KEY AUTO_INCREMENT,
#transaction_id INT NOT NULL,
#user_id_paid_by INT NOT NULL,
#method VARCHAR(45) NOT NULL,
#amount DECIMAL(65, 2) NOT NULL,
#date DATE NOT NULL,
#created_by INT NOT NULL,
#created_at DATE NOT NULL,
#FOREIGN KEY (transaction_id) REFERENCES transactions(id),
#FOREIGN KEY (user_id_paid_by) REFERENCES users(id),
#FOREIGN KEY (created_by) REFERENCES users(id)
#);
class Payments:
    def __init__(self, transaction_id, user_id_paid_by, method, amount, date, created_by) -> None:
        self.transaction_id = transaction_id
        self.user_id_paid_by = user_id_paid_by
        self.method = method
        self.amount = amount
        self.date = date
        self.created_by = created_by
        self.created_at = datetime.date.today()
        self.id = None

    def save(self):
        db = con.connect(
            user = 'root',
            host = 'localhost',
            database = 'test1',
            passwd = 'r00tP45s!'
        )

        cur = db.cursor()
        sql = "INSERT INTO payments (transaction_id, user_id_paid_by, method, amount, date, created_by, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cur.execute(sql, (self.transaction_id, self.user_id_paid_by, self.method, self.amount, self.date, self.created_by, self.created_at))

        db.commit()
        self.id = cur.lastrowid
        cur.close()
        db.close()

    @classmethod
    def create(cls, transaction_id, user_id_paid_by, method, amount, date, created_by):
        new_instance = cls(transaction_id, user_id_paid_by, method, amount, date, created_by)
        new_instance.save()

        return new_instance