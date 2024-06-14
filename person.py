import mysql.connector as con
import datetime
#cur.execute("CREATE TABLE Persons (id int PRIMARY KEY AUTO_INCREMENT, name varchar(50) NOT NULL, phone varchar(13) NOT NULL, email varchar(50) NOT NULL, created_at datetime NOT NULL, modified_at datetime)")

def displayUsers():
    db = con.connect(
        user = 'root',
        host = 'localhost',
        database = 'test1',
        passwd = 'r00tP45s!'
    )

    cur = db.cursor()
    cur.execute("SELECT id , name FROM persons")
    res = cur.fetchall()
    for name in res:
        print(name, '\n')
    
    db.commit()
    cur.close()
    db.close()
def save():
    db = con.connect(
        user = 'root',
        host = 'localhost',
        database = 'test1',
        passwd = 'r00tP45s!'
    )

    cur = db.cursor()

    name = input("Enter the name: ")
    phone = input("Enter the phone number: ")
    email = input("Enter the email: ")
    sql = "INSERT INTO Persons (name, phone, email, created_at) VALUES (%s, %s, %s, %s)"

    cur.execute(sql, (name, phone, email, datetime.date.today()))

    db.commit()
    cur.close()
    db.close()

class Person:
    def __init__(self, ID: None, name: str, phone: str, email: str, created_at: str, modified_at: str) -> None:
        self.name = name
        self.phone = phone
        self.email = email
        self.created_at = created_at
        self.modified_at = modified_at
        self.ID = ID
        
    