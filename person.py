import mysql.connector as con
import datetime
#cur.execute("CREATE TABLE Persons (id int PRIMARY KEY AUTO_INCREMENT, name varchar(50) NOT NULL, phone_number varchar(45) NOT NULL, email varchar(255) NOT NULL, create_time TIMESTAMP NOT NULL)")

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
    


class Person:
    def __init__(self, name: str, phone_number: str, email: str) -> None:
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.create_time = datetime.date.today()
        self.ID = None

    def save(self):
        db = con.connect(
            user = 'root',
            host = 'localhost',
            database = 'test1',
            passwd = 'r00tP45s!'
        )

        cur = db.cursor()
        sql = "INSERT INTO Persons (name, phone_number, email, create_time) VALUES (%s, %s, %s, %s)"
        cur.execute(sql, (self.name, self.phone_number, self.email, self.create_time))

        db.commit()
        self.ID = cur.lastrowid
        cur.close()
        db.close()

    @classmethod
    def create(cls, name, phone_number, email):
        new_instance = cls(name, phone_number, email)
        new_instance.save()

        return new_instance
    
    

       
    