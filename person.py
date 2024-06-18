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
    


class Person:
    def __init__(self, name: str, phone: str, email: str) -> None:
        self.name = name
        self.phone = phone
        self.email = email
        self.created_at = datetime.date.today()
        self.modified_at = None
        self.ID = None

    def save(self):
        db = con.connect(
            user = 'root',
            host = 'localhost',
            database = 'test1',
            passwd = 'r00tP45s!'
        )

        cur = db.cursor()
        sql = "INSERT INTO Persons (name, phone, email, created_at) VALUES (%s, %s, %s, %s)"
        cur.execute(sql, (self.name, self.phone, self.email, self.created_at))

        db.commit()
        self.ID = cur.lastrowid
        cur.close()
        db.close()

    @classmethod
    def create(cls, name, phone, email):
        new_instance = cls(name, phone, email)
        new_instance.save()

        return new_instance
    
    

       
    