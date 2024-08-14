import database
import datetime
import transactions as tran
import users

chargeTable = {}

class Charges:
    def __init__(self, id, server_id, transaction_id, user_id_charge_affected, amount, created_by, created_at=None, modified_by=None, modified_at=None) -> None:
        self.id = id
        self.server_id = server_id
        self.transaction_id = transaction_id
        self.user_id_charge_affected = user_id_charge_affected
        self.amount = amount
        self.created_by = created_by
        self.created_at = created_at if created_at is not None else datetime.date.today()
        self.modified_at = modified_at
        self.modified_by = modified_by

    def save(self):
        db = database.Database()

        sql = """INSERT INTO charges (server_id, transaction_id, user_id_charge_affected, amount, created_by, created_at) 
                 VALUES (%s, %s, %s, %s, %s, %s)"""
        db.cur.execute(sql, (self.server_id, self.transaction_id, self.user_id_charge_affected, self.amount, self.created_by, self.created_at))

        db.connection.commit()
        self.id = db.cur.lastrowid
        chargeTable[self.id] = self
        db.close()

    @classmethod
    def create(cls, server_id, transaction_id, user_id_charge_affected, amount, created_by, created_at=None, modified_by=None, modified_at=None):
        new_instance = cls(None, server_id, transaction_id, user_id_charge_affected, amount, created_by, created_at, modified_by, modified_at)
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

def dues(server_id, user_dues, specify_user):
    db = database.Database()

    sql = '''SELECT transactions.id, charges.id FROM transactions
            LEFT JOIN charges 
            ON charges.transaction_id = transactions.id
            WHERE charges.user_id_charge_affected = %s 
            AND transactions.user_id_paid_by = %s
            AND charges.server_id = %s;'''
    
    db.cur.execute(sql, (user_dues, specify_user, server_id))
    res = db.cur.fetchall()
    tranList = []
    chargeList = []
    for dues in res:
        tranList.append(tran.transactionTable[int(dues[0])])
        chargeList.append(chargeTable[int(dues[1])])

    output = []

    if not tranList:
        output.append("There are no charges to " + users.showUser(int(user_dues)) + " from " + users.showUser(int(specify_user)))
    else:
        output.append("Charges to " + users.showUser(int(user_dues)))
        output.append("----------------------------")
        for t, c in zip(tranList, chargeList):
            output.append("$" + f"{c.amount:.2f}" + " for " + t.description)
        output.append("")

    sql = '''SELECT transactions.id, charges.id FROM transactions
            LEFT JOIN charges 
            ON charges.transaction_id = transactions.id
            WHERE charges.user_id_charge_affected = %s 
            AND transactions.user_id_paid_by = %s
            AND charges.server_id = %s;'''
    
    db.cur.execute(sql, (specify_user, user_dues, server_id))
    res = db.cur.fetchall()
    tranList.clear()
    chargeList.clear()
    for dues in res:
        tranList.append(tran.transactionTable[int(dues[0])])
        chargeList.append(chargeTable[int(dues[1])])

    if not tranList:
        output.append("There are no charges to " + users.showUser(int(specify_user)) + " from " + users.showUser(int(user_dues)))
    else:
        output.append("Charges to " + users.showUser(int(specify_user)))
        output.append("----------------------------")
        for t, c in zip(tranList, chargeList):
            output.append("$" + f"{c.amount:.2f}" + " for " + t.description)

    db.close()

    return "\n".join(output)
