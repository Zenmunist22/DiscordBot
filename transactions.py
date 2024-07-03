import mysql.connector as con
import users
import datetime
#CREATE TABLE Transactions (id int PRIMARY KEY AUTO_INCREMENT, transaction_category_id INT NOT NULL, user_id_paid_by INT NOT NULL, DECIMAL(65,2) NOT NULL, source VARCHAR(255) NOT NULL, split_to_users INT NOT NULL, description VARCHAR(45) NOT NULL, date DATE NOT NULL, updated_at TIMESTAMP, created_at TIMESTAMP NOT NULL, created_by INT NOT NULL, updated_by INT, FOREIGN KEY (user_id_paid_by) REFERENCES users(id) , FOREIGN KEY (split_to_users) REFERENCES users(id) , FOREIGN KEY (created_by) REFERENCES users(id), FOREIGN KEY (updated_by) REFERENCES users(id), FOREIGN KEY (transaction_category_id) REFERENCES transaction_category(id));
#CREATE TABLE transaction_category (id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(45) NOT NULL, created_at DATE NOT NULL);
#INSERT INTO transaction_category (name, created_at) values ("Grocery", CURDATE()), ("Rent",CURDATE()), ("Furniture",CURDATE()), ("Supply",CURDATE()), ("Other", CURDATE());
def displayCategories():
    db = con.connect(
        user = 'root',
        host = 'localhost',
        database = 'test1',
        passwd = 'r00tP45s!'
    )

    cur = db.cursor()
    cur.execute("SELECT id , name FROM transaction_category")
    res = cur.fetchall()
    for name in res:
        print(name, '\n')
    
    db.commit()
    cur.close()
    db.close()

def displaySpecifiedTransactions(currently_paying, being_paid):
    db = con.connect(
        user = 'root',
        host = 'localhost',
        database = 'test1',
        passwd = 'r00tP45s!'
    )

    cur = db.cursor()
    sql = '''SELECT transactions.id , transactions.source, transactions.description, charges.amount FROM transactions
            LEFT JOIN charges 
            ON charges.transaction_id = transactions.id
            WHERE charges.user_id_charge_affected = %s 
            AND transactions.user_id_paid_by = %s; '''
    cur.execute(sql, (currently_paying, being_paid))
    res = cur.fetchall()
    for charge in res:
        print(charge, '\n')
    
    db.commit()
    cur.close()
    db.close()

class Transactions:
    def __init__(self, transaction_category_id, user_id_paid_by, amount, source, split_to_users, description, date, created_by) -> None:
        self.transaction_category_id = transaction_category_id
        self.user_id_paid_by = user_id_paid_by
        self.amount = amount
        self.source = source
        self.split_to_users = split_to_users
        self.description = description
        self.created_by = created_by
        self.created_at = datetime.datetime.now()
        self.updated_by = None
        self.updated_at = None
        self.date = date
        self.id = None

    def save(self):
        db = con.connect(
            user = 'root',
            host = 'localhost',
            database = 'test1',
            passwd = 'r00tP45s!'
        )

        cur = db.cursor()
        sql = "INSERT INTO Transactions (transaction_category_id, user_id_paid_by, amount, source, split_to_users, description, date, created_by, created_at) VALUES (%s, %s, %s, %s , %s , %s , %s , %s , %s)"
        cur.execute(sql, (self.transaction_category_id, self.user_id_paid_by, self.amount, self.source, self.split_to_users, self.description, self.date, self.created_by, self.created_at))

        db.commit()
        self.id = cur.lastrowid
        cur.close()
        db.close()
            
    @classmethod
    def create(cls, transaction_category_id, user_id_paid_by, amount, source, split_to_users, description, date, created_by):
        new_instance = cls(transaction_category_id, user_id_paid_by, amount, source, split_to_users, description, date, created_by)
        new_instance.save()

        return new_instance
        