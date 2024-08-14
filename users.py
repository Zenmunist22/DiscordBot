import mysql.connector as con
import datetime
import database

usersTable = {}

# User class
class User:
    def __init__(self, id: int, server_id: int, specific_id: int, name: str, phone_number: str, email: str, create_time=None) -> None:
        self.id = id
        self.server_id = server_id
        self.specific_id = specific_id
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.create_time = create_time if create_time is not None else datetime.date.today()

    def save(self):
        db = database.Database()
        # Insert user with server_id and server_specific_id
        sql = """INSERT INTO Users (server_id, server_specific_id, name, phone_number, email, create_time) 
                 VALUES (%s, %s, %s, %s, %s, %s)"""
        db.cur.execute(sql, (self.server_id, self.specific_id, self.name, self.phone_number, self.email, self.create_time))

        db.connection.commit()
        self.id = db.cur.lastrowid
        usersTable[self.id] = self
        db.close()

    @classmethod
    def create(cls, server_id, name, phone_number, email):
        db = database.Database()

        # Get the next server_specific_id for the server
        sql = """SELECT COALESCE(MAX(server_specific_id), 0) + 1 FROM users WHERE server_id = %s"""
        db.cur.execute(sql, (server_id,))
        specific_id = db.cur.fetchone()[0]

        new_instance = cls(None, server_id, specific_id, name, phone_number, email)
        db.close()
        new_instance.save()

        return new_instance

# User Functions
def fetchUsers():
    db = database.Database()
    db.cur.execute("SELECT * FROM users")
    results = db.cur.fetchall()
    users = [User(*result) for result in results]
    db.close()
    return users

def get_user_id(server_id, specific_id):
    for user in usersTable.values():
        if user.server_id == server_id and user.specific_id == specific_id:
            return user.id
    return None

# Create User list. Not permanent location
users_list = fetchUsers()
usersTable = {user.id: user for user in users_list}

def showUser(ID):
    return f"{usersTable[ID].name}"

def displayUsers(server_id: int, option=None):
    if option:
        res = set()
        for user in usersTable.values():
            if user.server_id == server_id:
                res.add(user.name)
        return res
    user_display = []
    for user in usersTable.values():
        if user.server_id == server_id:
            user_display.append(f"{user.specific_id}. {user.name}")
    return "\n".join(user_display)
