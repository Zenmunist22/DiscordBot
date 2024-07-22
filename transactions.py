import database
import users
import datetime


transactionTable = {}

#class trans
class Transactions:
    def __init__(self, id, transaction_category_id, user_id_paid_by, amount, source, split_to_users, description, date, updated_at, created_at, created_by, updated_by=None) -> None:
        self.transaction_category_id = transaction_category_id
        self.user_id_paid_by = user_id_paid_by
        self.amount = amount
        self.source = source
        self.split_to_users = split_to_users
        self.description = description
        self.created_by = created_by
        self.created_at = created_at if created_at is not None else datetime.date.today()
        self.updated_by = updated_by
        self.updated_at = updated_at
        self.date = date
        self.id = id

    def save(self):
        db = database.Database()

        sql = "INSERT INTO Transactions (transaction_category_id, user_id_paid_by, amount, source, split_to_users, description, date, created_at, created_by) VALUES (%s, %s, %s, %s , %s , %s , %s , %s , %s)"
        db.cur.execute(sql, (self.transaction_category_id, self.user_id_paid_by, self.amount, self.source, self.split_to_users, self.description, self.date, self.created_at, self.created_by))

        db.connection.commit()
        self.id = db.cur.lastrowid
        transactionTable[self.id] = self
        db.close()
            
    @classmethod
    def create(cls, id, transaction_category_id, user_id_paid_by, amount, source, split_to_users, description, date,  updated_at, created_at, created_by):
        new_instance = cls(id, transaction_category_id, user_id_paid_by, amount, source, split_to_users, description, date,  updated_at, created_at, created_by)
        new_instance.save()

        return new_instance
        
#functions
def fetchTransactions():
    db = database.Database()
    db.cur.execute("SELECT * FROM transactions")
    results = db.cur.fetchall()
    transactions = [Transactions(*result) for result in results]

    db.close()
    return transactions

transaction_list = fetchTransactions()
transactionTable = {transaction.id: transaction for transaction in transaction_list}

def displayCategories():
    db = database.Database()

    db.cur.execute("SELECT id , name FROM transaction_category")
    res = db.cur.fetchall()
    cat = set()
    for name in res:
        print(str(name[0]) + ". " + name[1])
        cat.add(str(name[0]))
    
    db.close()
    return cat

def displaySpecifiedTransactions(currently_paying, being_paid):
    db = database.Database()
    sql = '''SELECT transactions.id FROM transactions
            LEFT JOIN charges 
            ON charges.transaction_id = transactions.id
            WHERE charges.user_id_charge_affected = %s 
            AND transactions.user_id_paid_by = %s; '''
    db.cur.execute(sql, (currently_paying, being_paid))
    res = db.cur.fetchall()
    temp = []
    for charge in res:
        temp.append(transactionTable[int(*charge)])
    for t in temp:
        print(str(t.id) + ". " + t.description + " for an amount of $" + str(t.amount) + " from " + str(t.date))
    db.close()
    

