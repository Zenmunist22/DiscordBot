import mysql.connector as con
import datetime
import database
 
#cur.execute("CREATE TABLE Users (id int PRIMARY KEY AUTO_INCREMENT, name varchar(50) NOT NULL, phone_number varchar(45) NOT NULL, email varchar(255) NOT NULL, create_time TIMESTAMP NOT NULL)")

#User class
class User:
    def __init__(self, id: any, name: str, phone_number: str, email: str, create_time=None) -> None:
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.create_time = create_time if create_time is not None else datetime.date.today()
        self.id = id

    def save(self):
        db = database.Database()
        sql = "INSERT INTO Users (name, phone_number, email, create_time) VALUES (%s, %s, %s, %s)"
        db.cur.execute(sql, (self.name, self.phone_number, self.email, self.create_time))

        db.connection.commit()
        self.id = db.cur.lastrowid
        db.close()

    @classmethod
    def create(cls, id, name, phone_number, email):
        new_instance = cls(id, name, phone_number, email)
        new_instance.save()

        return new_instance
    
#User Functions
def fetchUsers():
    db = database.Database()
    db.cur.execute("SELECT * FROM users")
    results = db.cur.fetchall()
    users = [User(*result) for result in results]

    db.close()
    return users

#Create User list. Not permanent location
users_list = fetchUsers()
usersTable = {user.id: user for user in users_list}

def displayUsers():
    for user in usersTable:
        print(str(user) + ". " + usersTable[user].name)
    
    