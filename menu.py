import user
import transactions
import charges
from payments import splitTransaction
flag = True
def new_expense():
    print("The expense falls under which category: ")
    transactions.displayCategories()
    transaction_category_id = int(input())
    print("Paid by: ")
    user.displayUsers()
    user_id_paid_by = int(input())
    amount = input("How much: ")
    source = input("Source of purchase: ")
    users_paying = []
    while flag:
        print("Who needs to pay: ")
        user.displayUsers()
        hold = input()
        print("Confirm charge to" + hold + "? (y/n)")
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
    split_to_users = int(input())
    description = input("Description: ")
    date = input("Date of purchase (YYYY-MM-DD): ")
    print("Created by: ")
    user.displayUsers()
    created_by = int(input())
    new_trans = transactions.Transactions.create(transaction_category_id, user_id_paid_by, amount, source, split_to_users, description, date, created_by)
    split = amount/len(users_paying)
    for user in users_paying:
        charges.Charges.create(new_trans.id, user, split, created_by)
    

def add_user():
    name = input("Enter the name: ")
    phone_number = input("Enter the phone number: ")
    email = input("Enter the email: ")
    test = user.User.create(name, phone_number, email)
    #print(str(test.id) + " " + test.email)

def display_dues():
    print("Whose dues would you like to see?"\
    '\nPlease select from the following options:\n\n')
    user.displayUsers()
    command = input()

while flag:
    command = input('Hi,' \
            '\nPlease select from the following options:\n\n' \
            '1. Enter new expense\n'\
            '2. View current household dues\n' \
            '3. Display monthly payment breakdown\n' \
            '4. Add User\n' \
            '5. Exit Program\n\n' \
            'Option Selected: ')

    match command:
        case "1":
            new_expense()
        case "2":
            display_dues()
        case "3":
            command = input("Sample amount: ")
            split = splitTransaction(int(command))
            print("Each of you owe $" + str(split))
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

