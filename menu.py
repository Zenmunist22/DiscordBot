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
    try:
        name = input("Enter the name: ").strip()
        if not name:
            raise ValueError("Name cannot be empty.")
        nameSet = users.displayUsers(1)
        if name in nameSet:
            raise ValueError("Name already taken. Try something else")

        phone_number = input("Enter the phone number: ")
        if not phone_number.isdigit():
            raise ValueError("Phone number must contain only digits.")
        if len(phone_number) < 7 or len(phone_number) > 15:
            raise ValueError("Phone number must be between 7 and 15 digits long.")

        email = input("Enter the email: ")
        if "@" not in email or "." not in email:
            raise ValueError("Email must be a valid email address.")

        users.User.create(None, name, phone_number, email)
        print("User created successfully!")

    except ValueError as e:
        print(f"Input error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def display_dues():
    try:
        print("Whose dues would you like to see?\nPlease select from the following options:\n")
        users.displayUsers()
        user_dues = input()
        if not user_dues.isdigit() or int(user_dues) not in users.usersTable:
            raise ValueError("Invalid user ID selected.")
        user_dues = int(user_dues)
        
        print(users.showUser(user_dues) + "'s Balance")
        print("----------------------------")
        
        total = 0
        for i in users.usersTable:
            if i == user_dues:
                continue
            total += seeBalance(user_dues, i, 1)
        
        print("\nTotal Balance: $" + str(total))
        print("----------------------------")
    
    except ValueError as e:
        print(f"Input error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def make_payment():
    try:
        print("Who is making the payment?")
        users.displayUsers()
        currently_paying = input()
        if not currently_paying.isdigit() or int(currently_paying) not in users.usersTable:
            raise ValueError("Invalid user ID for who is making the payment.")
        currently_paying = int(currently_paying)

        print("Who is the payment to? ")
        being_paid = input()
        if not being_paid.isdigit() or int(being_paid) not in users.usersTable:
            raise ValueError("Invalid user ID for who is being paid.")
        being_paid = int(being_paid)

        balance = seeBalance(currently_paying, being_paid, 2)
        
        if balance > 0 :
            print(users.showUser(int(currently_paying)) + " owes " + users.showUser(int(being_paid)) + " $" + str(balance))
        elif balance < 0:
            print(users.showUser(int(being_paid)) + " owes " + users.showUser(int(currently_paying)) + " $" + str(-1*balance))
        else:
            print("There is no debt between " + users.showUser(int(being_paid)) + " and " + users.showUser(int(currently_paying)))
            while True:
                cont = input("Would you like to continue with the payment? (y/n) ").strip().lower()
                if cont in ['y', 'n']:
                    break
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")
            if cont == "n":
                return

        while True:
            specific = input("Is the payment specific to one transaction? (y/n) ").strip().lower()
            if specific in ['y', 'n']:
                break
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

        if specific == "y":
            tSet = transactions.displaySpecifiedTransactions(currently_paying, being_paid)
            if tSet:
                print("Select from the following transactions: ")
                transaction_id = input()
                if not transaction_id.isdigit() or int(transaction_id) not in tSet:
                    raise ValueError("Invalid transaction ID.")
            else:
                print(f"There are no transactions where {users.showUser(int(currently_paying))} owes {users.showUser(int(being_paid))}")
                transaction_id = None
        else:
            transaction_id = None

        method = input("Payment method: ")
        if not method:
            raise ValueError("Payment method cannot be empty.")

        amount = input("Payment amount: ")
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Payment amount must be positive.")
        except ValueError:
            raise ValueError("Payment amount must be a valid number.")

        date = input("Payment date (YYYY-MM-DD): ")
        # Optional: Add date validation here

        print("Created by: ")
        users.displayUsers()
        created_by = input()
        if not created_by.isdigit() or int(created_by) not in users.usersTable:
            raise ValueError("Invalid user ID for created by.")
        created_by = int(created_by)

        payments.Payments.create(None, transaction_id, currently_paying, being_paid, method, amount, date, created_by, None)
        print("Payment created successfully!")
    except ValueError as e:
        print(f"Input error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def seeBalance(payer, payee, option):
    try:
        db = database.Database()
        
        sql = '''SELECT SUM(charges.amount) as total FROM transactions
                LEFT JOIN charges 
                ON charges.transaction_id = transactions.id
                WHERE charges.user_id_charge_affected = %s
                AND transactions.user_id_paid_by = %s;'''
        
        try:
            db.cur.execute(sql, (payer, payee))
            results = db.cur.fetchall()
            if not results or results[0] is None or results[0][0] is None:
                res = 0
            else:
                res = results[0][0]
            
            db.cur.execute(sql, (payee, payer))
            results = db.cur.fetchall()
            if results and results[0][0] is not None:
                res -= results[0][0]
        
        except Exception as e:
            print(f"An error occurred while fetching transactions: {e}")
            res = 0

        sql = '''SELECT SUM(payments.amount) as total FROM payments 
                WHERE user_id_paid_by = %s
                AND user_id_paid_to = %s;'''

        try:
            db.cur.execute(sql, (payer, payee))
            results = db.cur.fetchall()
            if not results or results[0] is None or results[0][0] is None:
                res2 = 0
            else:
                res2 = results[0][0]
            
            db.cur.execute(sql, (payee, payer))
            results = db.cur.fetchall()
            if results and results[0][0] is not None:
                res2 -= results[0][0]

        except Exception as e:
            print(f"An error occurred while fetching payments: {e}")
            res2 = 0

        balance = res - res2

        if option == 1:
            print(f"To {users.showUser(int(payee)):<5}\t${balance:.2f}")

        return balance

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return 0

    finally:
        db.close()

def displayCharges():
    try:
        print("Whose dues would you like to see?\nPlease select from the following options:\n")
        users.displayUsers()
        user_dues = input()
        if not user_dues.isdigit() or int(user_dues) not in users.usersTable:
            raise ValueError("Invalid user ID selected.")
        user_dues = int(user_dues)
        print("Dues between " + users.showUser(int(user_dues)) + " and who?"\
        '\nPlease select from the following options:\n')
        users.displayUsers()
        specifiy_user = input()
        if not specifiy_user.isdigit() or int(specifiy_user) not in users.usersTable:
            raise ValueError("Invalid user ID selected.")
        specifiy_user = int(specifiy_user)
        
        charges.dues(user_dues, specifiy_user)
    
    except ValueError as e:
        print(f"Input error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def displayPayments():
    try:
        print("Whose payments would you like to see?\nPlease select from the following options:\n")
        users.displayUsers()
        user_paid = input()
        if not user_paid.isdigit() or int(user_paid) not in users.usersTable:
            raise ValueError("Invalid user ID selected.")
        user_paid = int(user_paid)

        print("Payments to who?"\
        '\nPlease select from the following options:\n')
        users.displayUsers()
        specifiy_user = input()
        if not specifiy_user.isdigit() or int(specifiy_user) not in users.usersTable:
            raise ValueError("Invalid user ID selected.")
        specifiy_user = int(specifiy_user)

        payments.paid(user_paid, specifiy_user)
    
    except ValueError as e:
        print(f"Input error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    

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
            'Option Selected: ').strip()

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

