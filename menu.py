import transactions
import users
import charges
import payments
import database

flag = True

def new_expense():
    try:
        print("The expense falls under which category: ")
        cat = transactions.displayCategories()
        transaction_category_id = input()
        if not transaction_category_id.isdigit():
            raise ValueError("Category ID must be a number.")
        if transaction_category_id not in cat:
            raise ValueError("Category ID does not exist.")
        transaction_category_id = int(transaction_category_id)
        

        print("Paid by: ")
        users.displayUsers()
        user_id_paid_by = input()
        if not user_id_paid_by.isdigit():
            raise ValueError("User ID must be a number.")
        user_id_paid_by = int(user_id_paid_by)
        if user_id_paid_by not in users.usersTable:
            raise ValueError("User ID does not exist.")
        print("Paid by " + users.showUser(user_id_paid_by))

        amount = input("How much: ")
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Amount must be positive.")
        except ValueError:
            raise ValueError("Amount must be a valid number.")
        
        source = input("Source of purchase: ")
        if not source:
            raise ValueError("Source cannot be empty.")

        users_paying = []
        count = 0
        while True:
            print("Who needs to pay: ")
            users.displayUsers()
            hold = input()
            if not hold.isdigit() or int(hold) not in users.usersTable:
                print("Invalid user ID. Please enter a valid number.")
                continue
            user_id = int(hold)
            while True:
                print("Confirm charge to " + users.showUser(user_id) + "? (y/n) ")
                confirm = input().strip().lower()
                if confirm in ['y', 'n']:
                    break
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")
            if confirm == "y":
                users_paying.append(user_id)
                count += 1
            if count > 0:
                while True:
                    again = input("Charge another user? (y/n) ").strip().lower()
                    if again in ['y', 'n']:
                        break
                    else:
                        print("Invalid input. Please enter 'y' or 'n'.")
                if again == "n":
                    break

        description = input("Description: ")
        if not description:
            raise ValueError("Description cannot be empty.")
        date = input("Date of purchase (YYYY-MM-DD): ")

        print("Created by: ")
        users.displayUsers()
        created_by = input()
        if not created_by.isdigit() or int(created_by) not in users.usersTable:
            raise ValueError("User ID must be a valid number in the user list.")
        created_by = int(created_by)

        split_to_users = len(users_paying) + 1
        split = amount/split_to_users

        print("Confirm transaction:\n" +
            users.showUser(user_id_paid_by) + " paid $" + str(amount) + " for " + description)
        print("The following user(s) will be charged $" + str(split) + " each:")
        for user in users_paying:
            print(users.showUser(int(user)))
        
        confirm = input("Confirm? (y/n) ").strip().lower()
        if confirm == "n":
            cancel = input("Cancel transaction? (y/n) ").strip().lower()
            if cancel == "y":
                print("Transaction cancelled.")
                return

        new_trans = transactions.Transactions.create(None, transaction_category_id, user_id_paid_by, amount, source, split_to_users, description, date, None, None, created_by)
        
        for user in users_paying:
            charges.Charges.create(None, new_trans.id, user, split, created_by, None, None, None)

        print("Transaction created!")

    except ValueError as e:
        print(f"Input error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def add_user():
    name = input("Enter the name: ")
    phone_number = input("Enter the phone number: ")
    email = input("Enter the email: ")
    users.User.create(None, name, phone_number, email)

def display_dues():
    print("Whose dues would you like to see?"\
    '\nPlease select from the following options:\n')
    users.displayUsers()
    user_dues = input()
    print(users.showUser(int(user_dues)) + "'s Balance")
    print("----------------------------")
    total = 0
    for i in users.usersTable:
        if i == int(user_dues):
            continue
        total += seeBalance(user_dues, users.usersTable[i].id, 1)
    print("\nTotal Balance: $" + str(total))
    print("----------------------------")

def make_payment():

    print("Who is making the payment?")
    users.displayUsers()
    currently_paying = input()

    print("Who is the payment to? ")
    being_paid = input()

    balance = seeBalance(currently_paying, being_paid, 2)
    
    if balance > 0 :
        print(users.showUser(int(currently_paying)) + " owes " + users.showUser(int(being_paid)) + " $" + str(balance))
    elif balance < 0:
        print(users.showUser(int(being_paid)) + " owes " + users.showUser(int(currently_paying)) + " $" + str(-1*balance))
    else:
        print("There is no debt between " + users.showUser(int(being_paid)) + " and " + users.showUser(int(currently_paying)))
        cont = input("Would you like to add a transaction? (y/n) ")
        if cont == "y":
            new_expense()
        else:
            cont = input("Would you like to continue with the payment? (y/n) ")
            if cont == "n":
                return

    specific = input("Is the payment specific to one transaction? (y/n) ")

    if specific == "y":
        print("Select from the following transactions: ")
        transactions.displaySpecifiedTransactions(currently_paying, being_paid)
        transaction_id = input()
    else:
        transaction_id = None

    method = input("Payment method: ")
    amount = input("Payment amount: ")
    date = input("Payment date: ")

    print("Created by: ")
    users.displayUsers()
    created_by = input()
    
    payments.Payments.create(None, transaction_id, currently_paying, being_paid, method, int(amount), date, created_by, None)

def seeBalance(payer, payee, option):
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
    if option == 1:
        print( f"To {users.showUser(int(payee)):<5}\t${balance:.2f}")
    db.close()
    return balance

def displayCharges():
    print("Whose dues would you like to see?"\
    '\nPlease select from the following options:\n')
    users.displayUsers()
    user_dues = input()
    charges.dues(user_dues)

def displayPayments():
    print("Whose payments would you like to see?"\
    '\nPlease select from the following options:\n')
    users.displayUsers()
    user_paid = input()
    payments.paid(user_paid)
    

while flag:
    command = input('Hi,' \
            '\nPlease select from the following options:\n\n' \
            '1. Enter new expense\n'\
            '2. View current household dues\n' \
            '3. Make payment\n' \
            '4. Add User\n' \
            '5. View charges\n' \
            '6. View payments\n' \
            '7. Exit Program\n\n' \
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
            displayCharges()
        case "6":
            displayPayments()
        case "7":
            print("Bye!")
            exit()
        case _:
            command = input("Invalid input, would you like to try again? (y/n) ")
            if command != "y":
                print("ok bye")
                exit()

