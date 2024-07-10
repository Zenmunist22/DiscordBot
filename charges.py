import database
import datetime
import transactions as tran
import users
'''CREATE TABLE charges (id INT PRIMARY KEY AUTO_INCREMENT,
transaction_id INT NOT NULL,
user_id_charge_affected INT NOT NULL,
amount DECIMAL(65, 2) NOT NULL,
created_by INT NOT NULL,
created_at DATE NOT NULL,
modified_by INT,
modified_at DATE,
charge_status ENUM('Paid', 'Owed') NOT NULL DEFAULT 'Owed',
FOREIGN KEY (transaction_id) REFERENCES transactions(id),
FOREIGN KEY (user_id_charge_affected) REFERENCES users(id),
FOREIGN KEY (created_by) REFERENCES users(id),
FOREIGN KEY (modified_by) REFERENCES users(id)
);'''

    
class Charges:
    def __init__(self, id, transaction_id, user_id_charge_affected, amount, created_by, created_at=None, modified_by=None, modified_at=None, charge_status=None ) -> None:
        self.transaction_id = transaction_id
        self.user_id_charge_affected = user_id_charge_affected
        self.amount = amount
        self.created_by = created_by
        self.created_at = created_at if created_at is not None else datetime.date.today()
        self.modified_at = modified_at
        self.modified_by = modified_by
        self.charge_status = "Owed"
        self.id = id

    def save(self):
        db = database.Database()

        sql = "INSERT INTO charges (transaction_id, user_id_charge_affected, amount, created_by, created_at) VALUES (%s, %s, %s, %s, %s)"
        db.cur.execute(sql, (self.transaction_id, self.user_id_charge_affected, self.amount, self.created_by, self.created_at))

        db.connection.commit()
        self.id = db.cur.lastrowid
        db.close()

    @classmethod
    def create(cls, id, transaction_id, user_id_charge_affected, amount, created_by, created_at, modified_by, modified_at, charge_status):
        new_instance = cls(id, transaction_id, user_id_charge_affected, amount, created_by, created_at, modified_by, modified_at, charge_status)
        new_instance.save()

        return new_instance
    
def fetchCharges():
    db = database.Database()
    db.cur.execute("SELECT * FROM charges")
    results = db.cur.fetchall()
    charges = [Charges(*result) for result in results]

    db.close()
    return charges

charge_list = fetchCharges()
chargeTable = {charge.id: charge for charge in charge_list}

def dues(user_dues):
    db = database.Database()

    sql = '''SELECT transactions.id, charges.id FROM transactions
            LEFT JOIN charges 
            ON charges.transaction_id = transactions.id
            WHERE charges.user_id_charge_affected = %s; '''
    db.cur.execute(sql, (user_dues,))
    res = db.cur.fetchall()
    tranList = []
    chargeList = []
    for dues in res:
        tranList.append(tran.transactionTable[int(dues[0])])
        chargeList.append(chargeTable[int(dues[1])])
    print("Here are all the dues of " + users.usersTable[int(user_dues)].name)
    for (t, c) in zip(tranList, chargeList):
        print(" owes " + users.usersTable[t.user_id_paid_by].name + " $" + str(c.amount) + " for " + t.description)   
    print()

    sql = '''SELECT transactions.id, charges.id FROM transactions
            LEFT JOIN charges 
            ON charges.transaction_id = transactions.id
            WHERE transactions.user_id_paid_by = %s
            AND charges.id IS NOT NULL; '''
    db.cur.execute(sql, (user_dues,))
    res = db.cur.fetchall()
    tranList.clear()
    chargeList.clear()
    for dues in res:
        tranList.append(tran.transactionTable[int(dues[0])])
        chargeList.append(chargeTable[int(dues[1])])
    print("Here is what " + users.usersTable[int(user_dues)].name + " is owed")
    for (t, c) in zip(tranList, chargeList):
        print( users.usersTable[c.user_id_charge_affected].name + " owes $" + str(c.amount) + " for " + t.description)  

    db.close()