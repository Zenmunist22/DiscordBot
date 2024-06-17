import mysql.connector as con
import person
import datetime
#CREATE TABLE Transactions (id int PRIMARY KEY AUTO_INCREMENT, title varchar(50) NOT NULL, category ENUM('Food', 'Rent' , 'Funiture', 'Other')  NOT NULL, amount int NOT NULL, charged_to int NOT NULL,  charged_from int NOT NULL,  description varchar(50) NOT NULL,  created_by int NOT NULL, created_at datetime NOT NULL, modified_by int, modified_at datetime, due_date datetime NOT NULL, FOREIGN KEY (charged_to) REFERENCES persons(id) , FOREIGN KEY (charged_from) REFERENCES persons(id) , FOREIGN KEY (modified_by) REFERENCES persons(id), FOREIGN KEY (created_by) REFERENCES persons(id));


def save():
    db = con.connect(
        user = 'root',
        host = 'localhost',
        database = 'test1',
        passwd = 'r00tP45s!'
    )

    cur = db.cursor()

    title = input("Title for transaction: ")
    category = input("Category:\n Food (1)\n Rent (2)\n Funiture (3)\n Other (4)\n")
    amount = input("How much: ")
    print("Who paid: ")
    person.displayUsers()
    charged_to = int(input())
    charged_from = input("Charged from?? ")
    description = input("Description: ")
    created_by = input("(USER NAME): ")
    due_date = input("Due date (YYYY-MM-DD): ")
    

    sql = "INSERT INTO Transactions (title, category, amount, charged_to, charged_from, description_, created_by, created_at, due_date) VALUES (%s, %s, %s, %s , %s , %s , %s , %s , %s)"

    cur.execute(sql, (title, category, amount, charged_to, charged_from, description, created_by, datetime.date.today(), due_date))

    db.commit()
    cur.close()
    db.close()

class Transactions:
    def __init__(self, ID, title, category, amount, charged_to, charged_from, description, created_by, created_at, modified_by, modified_at, due_date) -> None:
        self.ID = ID
        self.title = title
        self.title = title
        self.amount = amount
        self.charged_to = charged_to
        self.charged_from = charged_from
        self.description = description
        self.created_by = created_by
        self.created_at = created_at
        self.modified_by = modified_by
        self.modified_at = modified_at
        self.due_date = due_date

        
    