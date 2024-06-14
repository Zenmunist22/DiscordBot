import person
from dues import option_2
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
            command = input("Enter the expense amount: ")
            print("Adding $" + command +  " to your balance\n")
        case "2":
            command = input("Whose dues would you like to see?"\
            '\nPlease select from the following options:\n\n' \
            '1. Tommy\n'\
            '2. Hiram\n' \
            '3. Hazel\n' \
            '4. Kyle\n' \
            '5. Michael\n' \
            '6. All\n' \
            'Option Selected: ')
            option_2(command)
        case "3":
            command = input("Sample amount: ")
            split = splitTransaction(int(command))
            print("Each of you owe $" + str(split))
        case "4":
            person.save()
            
        case "5":
            print("Bye!")
            exit()

        case _:
            command = input("Invalid input, would you like to try again? (y/n)")
            if command != "y":
                print("ok bye")
                exit()
