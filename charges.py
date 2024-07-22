import database
import datetime
import transactions as tran
import users

chargeTable = {}

class Charges:
    def __init__(self, id, transaction_id, user_id_charge_affected, amount, created_by, created_at=None, modified_by=None, modified_at=None ) -> None:
        self.transaction_id = transaction_id
        self.user_id_charge_affected = user_id_charge_affected
        self.amount = amount
        self.created_by = created_by
        self.created_at = created_at if created_at is not None else datetime.date.today()
        self.modified_at = modified_at
        self.modified_by = modified_by
        self.id = id

    def save(self):
        db = database.Database()

        sql = "INSERT INTO charges (transaction_id, user_id_charge_affected, amount, created_by, created_at) VALUES (%s, %s, %s, %s, %s)"
        db.cur.execute(sql, (self.transaction_id, self.user_id_charge_affected, self.amount, self.created_by, self.created_at))

        db.connection.commit()
        self.id = db.cur.lastrowid
        chargeTable[self.id] = self
        db.close()

    @classmethod
    def create(cls, id, transaction_id, user_id_charge_affected, amount, created_by, created_at, modified_by, modified_at):
        new_instance = cls(id, transaction_id, user_id_charge_affected, amount, created_by, created_at, modified_by, modified_at)
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

def dues(user_dues, specifiy_user):
    db = database.Database()

    sql = '''SELECT transactions.id, charges.id FROM transactions
            LEFT JOIN charges 
            ON charges.transaction_id = transactions.id
            WHERE charges.user_id_charge_affected = %s AND
            transactions.user_id_paid_by = %s; '''
    db.cur.execute(sql, (user_dues, specifiy_user))
    res = db.cur.fetchall()
    tranList = []
    chargeList = []
    for dues in res:
        tranList.append(tran.transactionTable[int(dues[0])])
        chargeList.append(chargeTable[int(dues[1])])
    if tranList == []:
        print("There are no charges to " + users.showUser(int(user_dues)) + " from " + users.showUser(int(specifiy_user)))
    else:
        print("Charges to " + users.showUser(int(user_dues)))
        print("----------------------------")
        for (t, c) in zip(tranList, chargeList):
            print("$" + str(c.amount) + " for " + t.description)   
    print()

    sql = '''SELECT transactions.id, charges.id FROM transactions
            LEFT JOIN charges 
            ON charges.transaction_id = transactions.id
            WHERE charges.user_id_charge_affected = %s AND
            transactions.user_id_paid_by = %s; '''
    
    db.cur.execute(sql, (specifiy_user, user_dues))
    res = db.cur.fetchall()
    tranList.clear()
    chargeList.clear()
    for dues in res:
        tranList.append(tran.transactionTable[int(dues[0])])
        chargeList.append(chargeTable[int(dues[1])])
    if tranList == []:
        print("There are no charges to " + users.showUser(int(specifiy_user)) + " from " + users.showUser(int(user_dues)))
    else:
        print("Charges to " + users.showUser(int(specifiy_user)))
        print("----------------------------")
        for (t, c) in zip(tranList, chargeList):
            print("$" + str(c.amount) + " for " + t.description)   

    db.close()