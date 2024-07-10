import database
import users
import datetime
'''CREATE TABLE payments (id INT PRIMARY KEY AUTO_INCREMENT,
transaction_id INT,
user_id_paid_by INT NOT NULL,
user_id_paid_to INT NOT NULL,
method VARCHAR(45) NOT NULL,
amount DECIMAL(65, 2) NOT NULL,
date DATE NOT NULL,
created_by INT NOT NULL,
created_at DATE NOT NULL,
FOREIGN KEY (transaction_id) REFERENCES transactions(id),
FOREIGN KEY (user_id_paid_by) REFERENCES users(id),
FOREIGN KEY (created_by) REFERENCES users(id),
FOREIGN KEY (user_id_paid_to) REFERENCES users(id)
);'''

class Payments:
    def __init__(self, id, transaction_id, user_id_paid_by, user_id_paid_to, method, amount, date, created_by, created_at) -> None:
        self.transaction_id = transaction_id
        self.user_id_paid_by = user_id_paid_by
        self.user_id_paid_to = user_id_paid_to
        self.method = method
        self.amount = amount
        self.date = date
        self.created_by = created_by
        self.created_at = created_at if created_at is not None else datetime.date.today()
        self.id = id

    def save(self):
        db = database.Database()

        sql = "INSERT INTO payments (transaction_id, user_id_paid_by, user_id_paid_to, method, amount, date, created_by, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        db.cur.execute(sql, (self.transaction_id, self.user_id_paid_by, self.user_id_paid_to, self.method, self.amount, self.date, self.created_by, self.created_at))

        db.connection.commit()
        self.id = db.cur.lastrowid
        db.close()

    @classmethod
    def create(cls, id, transaction_id, user_id_paid_by, user_id_paid_to, method, amount, date, created_by, created_at):
        new_instance = cls(id, transaction_id, user_id_paid_by, user_id_paid_to, method, amount, date, created_by, created_at)
        new_instance.save()

        return new_instance
    
def fetchPayments():
    db = database.Database()
    db.cur.execute("SELECT * FROM payments")
    results = db.cur.fetchall()
    payments = [Payments(*result) for result in results]

    db.close()
    return payments

payment_list = fetchPayments()
paymentTable = {payment.id: payment for payment in payment_list}