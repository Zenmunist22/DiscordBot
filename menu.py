import transactions
import users
import charges
import payments
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
    while flag:
        print("Who needs to pay: ")
        users.displayUsers()
        hold = input()
        print("Confirm charge to " + hold + "? (y/n)")
        confirm = input()
        if confirm == "y":
            users_paying.append(hold)
        if confirm == "n":
            pass
        again = input("Charge another user? (y/n)")
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
    new_trans = transactions.Transactions.create(transaction_category_id, user_id_paid_by, int(amount), source, split_to_users, description, date, created_by)
    split = float(amount)//(split_to_users)
    for user in users_paying:
        charges.Charges.create(new_trans.id, user, split, created_by)
    

def add_user():
    name = input("Enter the name: ")
    phone_number = input("Enter the phone number: ")
    email = input("Enter the email: ")
    test = users.User.create(name, phone_number, email)
    #print(str(test.id) + " " + test.email)

def display_dues():
    print("Whose dues would you like to see?"\
    '\nPlease select from the following options:\n\n')
    users.displayUsers()
    user_dues = input()
    charges.dues(user_dues)

def make_payment():
    print("Who is making the payment?")
    users.displayUsers()
    currently_paying = input()
    print("Who is the payment to? ")
    being_paid = input()
    print("Select from the following transactions: ")
    transactions.displaySpecifiedTransactions(currently_paying, being_paid)
    transaction_id = input()
    method = input("Payment method: ")
    amount = input("Payment amount: ")
    #if(int(amount) >= something), then update status to PAID instead of OWED. Subtract amount from Charge amount and update Modified attributes
    date = input("Payment date: ")
    print("Created by: ")
    users.displayUsers()
    created_by = input()
    payments.Payments.create(transaction_id, currently_paying, method, int(amount), date, created_by)

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

