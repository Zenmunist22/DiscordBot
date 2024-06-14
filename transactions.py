import mysql.connector as con
import person
cur.execute("CREATE TABLE Transactions (id int PRIMARY KEY AUTO_INCREMENT, title varchar(50) NOT NULL, category ENUM('Food', 'Rent' , 'Funiture', 'Other')  NOT NULL, amount int NOT NULL, charged_to varchar(50) NOT NULL,  charged_from varchar(50) NOT NULL,  description varchar(50) NOT NULL,  created_by varchar(50) NOT NULL, created_at datetime NOT NULL, modified_by datetime NOT NULL, modified_at datetime NOT NULL, due_date datetime NOT NULL")

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
    charged_to = input()
    charged_from = input("Charged from?? ")
    description = input("Description: ")
    created_by = input("(USER NAME): ")

    sql = "INSERT INTO Transactions (name, phone, email, created_at) VALUES (%s, %s, %s, %s)"

    cur.execute(sql, (name, phone, email, datetime.date.today()))

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

        
    