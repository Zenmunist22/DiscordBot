import person
import transactions
from option_3 import splitTransaction
flag = True
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
            title = input("Title for transaction: ")
            category = input("Category:\n Food (1)\n Rent (2)\n Funiture (3)\n Other (4)\n")
            amount = input("How much: ")
            print("Charged to: ")
            person.displayUsers()
            charged_to = int(input())
            charged_from = input("Charged from: ")
            description = input("Description: ")
            created_by = input("(USER NAME): ")
            due_date = input("Due date (YYYY-MM-DD): ")
            transactions.Transactions.create(title, category, amount, charged_to, charged_from, description, created_by, due_date)
        case "2":
            print("Whose dues would you like to see?"\
            '\nPlease select from the following options:\n\n')
            person.displayUsers()
            command = input()
        case "3":
            command = input("Sample amount: ")
            split = splitTransaction(int(command))
            print("Each of you owe $" + str(split))
        case "4":
            name = input("Enter the name: ")
            phone = input("Enter the phone number: ")
            email = input("Enter the email: ")
            person.Person.create(name, phone, email)
            
        case "5":
            print("Bye!")
            exit()

        case _:
            command = input("Invalid input, would you like to try again? (y/n)")
            if command != "y":
                print("ok bye")
                exit()
