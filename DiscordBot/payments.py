import database
import users
import datetime
import transactions as tran


paymentTable = {}

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
        paymentTable[self.id] = self
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

def paid(user_paid, specify_user):
    db = database.Database()

    sql = '''SELECT transactions.id, payments.id FROM transactions
            LEFT JOIN payments 
            ON payments.transaction_id = transactions.id
            WHERE payments.user_id_paid_by = %s AND
            payments.user_id_paid_to = %s ; '''
    
    db.cur.execute(sql, (user_paid, specify_user))
    res = db.cur.fetchall()
    tranList = []
    payList = []
    for p in res:
        tranList.append(tran.transactionTable[int(p[0])])
        payList.append(paymentTable[int(p[1])])

    sql = '''SELECT NULL, payments.id FROM payments
            WHERE payments.transaction_id IS NULL
            AND payments.user_id_paid_by = %s AND
            payments.user_id_paid_to = %s; '''
    db.cur.execute(sql, (user_paid, specify_user))
    res = db.cur.fetchall()
    
    for p in res:
        tranList.append(None)  # Use None instead of 0 for clarity
        payList.append(paymentTable[int(p[1])])

    output = []

    if not payList:
        output.append("There are no payments made by " + users.showUser(int(user_paid)) + " to " + users.showUser(int(specify_user)))
    else:
        output.append("Payments " + users.showUser(int(user_paid)) + " made to " + users.showUser(int(specify_user)))
        output.append("----------------------------")
        for t, p in zip(tranList, payList):
            if t is None:
                output.append(" $" + f"{p.amount:.2f}" + " on " + str(p.date))
            else: 
                output.append(" $" + f"{p.amount:.2f}" + " on " + str(p.date) + " for " + t.description)

    db.close()

    return "\n".join(output)
