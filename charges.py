import mysql.connector as con
import datetime
#CREATE TABLE charges (id INT PRIMARY KEY AUTO_INCREMENT,
#transaction_id INT NOT NULL,
#user_id_charge_affected INT NOT NULL,
#amount DECIMAL(2) NOT NULL,
#created_by INT NOT NULL,
#created_at DATE NOT NULL,
#modified_by INT,
#modified_at DATE,
#FOREIGN KEY (transaction_id) REFERENCES transactions(id),
#FOREIGN KEY (user_id_charge_affected) REFERENCES users(id),
#FOREIGN KEY (created_by) REFERENCES users(id),
#FOREIGN KEY (modified_by) REFERENCES users(id)
#);

class Charges:
    def __init__(self, transaction_id, user_id_charge_affected, amount, created_by) -> None:
        self.transaction_id = transaction_id
        self.user_id_charge_affected = user_id_charge_affected
        self.amount = amount
        self.created_by = created_by
        self.created_at = datetime.date.today()
        self.modified_at = None
        self.modified_by = None
        self.id = None

    def save(self):
        db = con.connect(
            user = 'root',
            host = 'localhost',
            database = 'test1',
            passwd = 'r00tP45s!'
        )

        cur = db.cursor()
        sql = "INSERT INTO charges (transaction_id, user_id_charge_affected, amount, created_by, created_at) VALUES (%s, %s, %s, %s, %s)"
        cur.execute(sql, (self.transaction_id, self.user_id_charge_affected, self.amount, self.created_by, self.created_at))

        db.commit()
        self.id = cur.lastrowid
        cur.close()
        db.close()

    @classmethod
    def create(cls, transaction_id, user_id_charge_affected, amount, created_by):
        new_instance = cls(transaction_id, user_id_charge_affected, amount, created_by)
        new_instance.save()

        return new_instance