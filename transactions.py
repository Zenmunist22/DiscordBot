import database
import users
import datetime

transactionTable = {}

class Transactions:
    def __init__(self, id, server_id, server_specific_id, transaction_category_id, user_id_paid_by, amount, source, split_to_users, description, date, updated_at, created_at, created_by, updated_by=None) -> None:
        self.id = id
        self.server_id = server_id
        self.server_specific_id = server_specific_id
        self.transaction_category_id = transaction_category_id
        self.user_id_paid_by = user_id_paid_by
        self.amount = amount
        self.source = source
        self.split_to_users = split_to_users
        self.description = description
        self.date = date
        self.created_at = created_at if created_at is not None else datetime.date.today()
        self.updated_at = updated_at
        self.created_by = created_by
        self.updated_by = updated_by

    def save(self):
        db = database.Database()

        # Insert transaction with server_id and server_specific_id
        sql = """INSERT INTO Transactions (server_id, server_specific_id, transaction_category_id, user_id_paid_by, amount, source, split_to_users, description, date, created_at, created_by) 
                 VALUES (%s, %s, %s, %s , %s , %s , %s , %s , %s , %s)"""
        db.cur.execute(sql, (self.server_id, self.server_specific_id, self.transaction_category_id, self.user_id_paid_by, self.amount, self.source, self.split_to_users, self.description, self.date, self.created_at, self.created_by))

        db.connection.commit()
        self.id = db.cur.lastrowid
        transactionTable[self.id] = self
        db.close()

    @classmethod
    def create(cls, server_id, transaction_category_id, user_id_paid_by, amount, source, split_to_users, description, date, updated_at, created_at, created_by):
        db = database.Database()

        # Get the next server_specific_id for the server
        sql = """SELECT COALESCE(MAX(server_specific_id), 0) + 1 FROM transactions WHERE server_id = %s"""
        db.cur.execute(sql, (server_id,))
        server_specific_id = db.cur.fetchone()[0]

        new_instance = cls(None, server_id, server_specific_id, transaction_category_id, user_id_paid_by, amount, source, split_to_users, description, date, updated_at, created_at, created_by)
        db.close()
        new_instance.save()
        return new_instance

# functions
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
    categories = []
    cat_set = set()
    for name in res:
        categories.append(f"{name[0]}. {name[1]}")
        cat_set.add(str(name[0]))
    db.close()
    return "\n".join(categories), cat_set

def displaySpecifiedTransactions(server_id, currently_paying, being_paid):
    db = database.Database()
    s = set()
    
    sql = '''SELECT transactions.id FROM transactions
            LEFT JOIN charges 
            ON charges.transaction_id = transactions.id
            WHERE charges.user_id_charge_affected = %s 
            AND transactions.user_id_paid_by = %s
            AND transactions.server_id = %s; '''
    
    db.cur.execute(sql, (currently_paying, being_paid, server_id))
    res = db.cur.fetchall()
    
    temp = []
    output = []
    
    for charge in res:
        temp.append(transactionTable[int(*charge)])
    
    if not temp:
        output.append(f"No transactions found between {users.showUser(currently_paying)} and {users.showUser(being_paid)}.")
    else:
        output.append("----------------------------")
        for t in temp:
            output.append(str(t.server_specific_id) + f". {t.description} for an amount of ${t.amount/t.split_to_users:.2f} from {t.date}")
            s.add(t.server_specific_id)

    db.close()
    
    return "\n".join(output), s
