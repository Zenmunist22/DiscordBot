import person
import transactions
from DiscordBot.payments import splitTransaction
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
            print("The expense falls under which category: ")
            transactions.displayCategories()
            transaction_category_id = int(input())
            print("Paid by: ")
            person.displayUsers()
            user_id_paid_by = int(input())
            amount = input("How much: ")
            source = input("Source: ")
            print("Split TEST: ")
            person.displayUsers()
            split_to_persons = int(input())
            description = input("Description: ")
            date = input("Date of purchase (YYYY-MM-DD): ")
            print("Created by: ")
            person.displayUsers()
            created_by = int(input())
            transactions.Transactions.create(transaction_category_id, user_id_paid_by, amount, source, split_to_persons, description, date, created_by)
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
            phone_number = input("Enter the phone number: ")
            email = input("Enter the email: ")
            person.Person.create(name, phone_number, email)
            
        case "5":
            print("Bye!")
            exit()

        case _:
            command = input("Invalid input, would you like to try again? (y/n)")
            if command != "y":
                print("ok bye")
                exit()
