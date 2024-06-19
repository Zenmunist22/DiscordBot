import mysql.connector as con
import person
import datetime
#CREATE TABLE Transactions (id int PRIMARY KEY AUTO_INCREMENT, transaction_category_id INT NOT NULL, user_id_paid_by INT NOT NULL, amount DECIMAL(2) NOT NULL, source VARCHAR(255) NOT NULL, split_to_persons INT NOT NULL, description VARCHAR(45) NOT NULL, date DATE NOT NULL, updated_at TIMESTAMP, created_at TIMESTAMP NOT NULL, created_by INT NOT NULL, updated_by INT, FOREIGN KEY (user_id_paid_by) REFERENCES persons(id) , FOREIGN KEY (split_to_persons) REFERENCES persons(id) , FOREIGN KEY (created_by) REFERENCES persons(id), FOREIGN KEY (updated_by) REFERENCES persons(id), FOREIGN KEY (transaction_category_id) REFERENCES transaction_category(id));
#CREATE TABLE transaction_category (id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(45) NOT NULL, created_at DATE NOT NULL)
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

class Transactions:
    def __init__(self, transaction_category_id, user_id_paid_by, amount, source, split_to_persons, description, date, created_by) -> None:
        self.transaction_category_id = transaction_category_id
        self.user_id_paid_by = user_id_paid_by
        self.amount = amount
        self.source = source
        self.split_to_persons = split_to_persons
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
        sql = "INSERT INTO Transactions (transaction_category_id, user_id_paid_by, amount, source, split_to_persons, description, date, created_by, created_at) VALUES (%s, %s, %s, %s , %s , %s , %s , %s , %s)"
        cur.execute(sql, (self.transaction_category_id, self.user_id_paid_by, self.amount, self.source, self.split_to_persons, self.description, self.date, self.created_by, self.created_at))

        db.commit()
        cur.close()
        db.close()
            
    @classmethod
    def create(cls, transaction_category_id, user_id_paid_by, amount, source, split_to_persons, description, date, created_by):
        new_instance = cls(transaction_category_id, user_id_paid_by, amount, source, split_to_persons, description, date, created_by)
        new_instance.save()

        return new_instance
        