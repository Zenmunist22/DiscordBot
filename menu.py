import transactions
import users
import charges
import payments
import database
'''SELECT SUM(payments.amount) as total FROM transactions
            LEFT JOIN payments 
            ON payments.transaction_id = transactions.id
            WHERE payments.user_id_paid_by = %s
            AND transactions.user_id_paid_by = %s;'''
flag = True

def new_expense():
    print("The expense falls under which category: ")
    transactions.displayCategories()
    transaction_category_id = int(input())
    print("Paid by: ")
    users.displayUsers()
    user_id_paid_by = int(input())
    amount = input("How much: ")
    source = input("Source of purchase: ")
    users_paying = []
    while True:
        print("Who needs to pay: ")
        users.displayUsers()
        hold = input()
        print("Confirm charge to " + hold + "? (y/n)")
        confirm = input()
        if confirm == "y":
            users_paying.append(hold)
        if confirm == "n":
            pass
        again = input("Charge another user? (y/n) ")
        if again == "y":
            pass
        if again == "n":
            break
    description = input("Description: ")
    date = input("Date of purchase (YYYY-MM-DD): ")
    print("Created by: ")
    users.displayUsers()
    created_by = int(input())
    split_to_users = len(users_paying) + 1
    new_trans = transactions.Transactions.create(None, transaction_category_id, user_id_paid_by, int(amount), source, split_to_users, description, date, None, None, created_by)
    split = float(amount)//(split_to_users)
    for user in users_paying:
        charges.Charges.create(None, new_trans.id, user, split, created_by, None, None, None, None)
    

def add_user():
    name = input("Enter the name: ")
    phone_number = input("Enter the phone number: ")
    email = input("Enter the email: ")
    test = users.User.create(None, name, phone_number, email)
    #print(str(test.id) + " " + test.email)

def display_dues():
    print("Whose dues would you like to see?"\
    '\nPlease select from the following options:\n\n')
    users.displayUsers()
    user_dues = input()
    charges.dues(user_dues)
    print("")
    for i in users.usersTable:
        balanceCalc(user_dues, users.usersTable[i].id)

def make_payment():

    print("Who is making the payment?")
    users.displayUsers()
    currently_paying = input()

    print("Who is the payment to? ")
    being_paid = input()

    specific = input("Is the payment specific to one transaction? (y/n)")

    if specific == "y":
        print("Select from the following transactions: ")
        transactions.displaySpecifiedTransactions(currently_paying, being_paid)
        transaction_id = input()
    else:
        transaction_id = None
    balanceCalc(currently_paying, being_paid)
    method = input("Payment method: ")
    amount = input("Payment amount: ")
    #if(int(amount) >= something), then update status to PAID instead of OWED. Subtract amount from Charge amount and update Modified attributes
    date = input("Payment date: ")

    print("Created by: ")
    users.displayUsers()
    created_by = input()
    
    payments.Payments.create(None, transaction_id, currently_paying, being_paid, method, int(amount), date, created_by, None)

def balanceCalc(payer, payee):
    db = database.Database()
    sql = '''SELECT SUM(charges.amount) as total FROM transactions
            LEFT JOIN charges 
            ON charges.transaction_id = transactions.id
            WHERE charges.user_id_charge_affected = %s
            AND transactions.user_id_paid_by = %s;'''
    db.cur.execute(sql, (payer, payee))
    results = db.cur.fetchall()
    if results is None or results[0] is None or results[0][0] is None:
        res = 0
    else:
        res = results[0][0]
    db.cur.execute(sql, (payee, payer))
    results = db.cur.fetchall()
    if results[0][0] is not None:
        res = res - results[0][0]
    sql = '''SELECT SUM(payments.amount) as total FROM payments 
            WHERE user_id_paid_by = %s
            AND user_id_paid_to = %s;'''
    db.cur.execute(sql, (payer, payee))
    results = db.cur.fetchall()
    if results is None or results[0] is None or results[0][0] is None:
        res2 = 0
    else:
        res2 = results[0][0]
    db.cur.execute(sql, (payee, payer))
    results = db.cur.fetchall()
    if results[0][0] is not None:
        res2 = res2 - results[0][0]
    balance = res - res2
    if balance > 0 :
        print(users.usersTable[int(payer)].name + " owes " + users.usersTable[int(payee)].name + " $" + str(balance))
    elif balance < 0:
        print(users.usersTable[int(payee)].name + " owes " + users.usersTable[int(payer)].name + " $" + str(-1*balance))
    else:
        print("There is no debt between " + users.usersTable[int(payee)].name + " and " + users.usersTable[int(payer)].name)
    

    db.close()
    

while flag:
    command = input('Hi,' \
            '\nPlease select from the following options:\n\n' \
            '1. Enter new expense\n'\
            '2. View current household dues\n' \
            '3. Make payment\n' \
            '4. Add User\n' \
            '5. Exit Program\n\n' \
            'Option Selected: ')

    match command:
        case "1":
            new_expense()
        case "2":
            display_dues()
        case "3":
            make_payment()
        case "4":
            add_user()
        case "5":
            print("Bye!")
            exit()
        case _:
            command = input("Invalid input, would you like to try again? (y/n)")
            if command != "y":
                print("ok bye")
                exit()

