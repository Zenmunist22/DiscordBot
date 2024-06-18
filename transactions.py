import mysql.connector as con
import person
import datetime
#CREATE TABLE Transactions (id int PRIMARY KEY AUTO_INCREMENT, title varchar(50) NOT NULL, category ENUM('Food', 'Rent' , 'Funiture', 'Other')  NOT NULL, amount int NOT NULL, charged_to int NOT NULL,  charged_from int NOT NULL,  description varchar(50) NOT NULL,  created_by int NOT NULL, created_at datetime NOT NULL, modified_by int, modified_at datetime, due_date datetime NOT NULL, FOREIGN KEY (charged_to) REFERENCES persons(id) , FOREIGN KEY (charged_from) REFERENCES persons(id) , FOREIGN KEY (modified_by) REFERENCES persons(id), FOREIGN KEY (created_by) REFERENCES persons(id));

class Transactions:
    def __init__(self, title, category, amount, charged_to, charged_from, description, created_by, due_date) -> None:
        self.title = title
        self.category = category
        self.amount = amount
        self.charged_to = charged_to
        self.charged_from = charged_from
        self.description = description
        self.created_by = created_by
        self.created_at = datetime.date.today()
        self.modified_by = None
        self.modified_at = None
        self.due_date = due_date
        self.ID = None

    def save(self):
        db = con.connect(
            user = 'root',
            host = 'localhost',
            database = 'test1',
            passwd = 'r00tP45s!'
        )

        cur = db.cursor()
        sql = "INSERT INTO Transactions (title, category, amount, charged_to, charged_from, description, created_by, created_at, due_date) VALUES (%s, %s, %s, %s , %s , %s , %s , %s , %s)"
        cur.execute(sql, (self.title, self.category, self.amount, self.charged_to, self.charged_from, self.description, self.created_by, self.created_at, self.due_date))

        db.commit()
        cur.close()
        db.close()
            
    @classmethod
    def create(cls, title, category, amount, charged_to, charged_from, description, created_by, due_date):
        new_instance = cls(title, category, amount, charged_to, charged_from, description, created_by, due_date)
        new_instance.save()

        return new_instance
        