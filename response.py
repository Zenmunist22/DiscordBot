
import users
def get_response(command) -> str:
    command = command.lower()

    if command == "!start":
        return ('Hi,' \
            '\nPlease select from the following options:\n\n' \
            '1. Enter new expense\n'\
            '2. View current household dues\n' \
            '3. Make payment\n' \
            '4. Add User\n' \
            '5. View charges\n' \
            '6. View payments\n' \
            '7. Exit Program\n\n' \
            'Option Selected: ').strip()
    if command != "4" and command != "7" and len(users.usersTable) < 2: 
        print("Enter least two users before using these features! ")

    match command:
        case "4":
            pass
        case "7":
            print("Bye!")
            exit()
        case _:
            command = input("Invalid input, would you like to try again? (y/n) ").strip().lower()
            if command != "y":
                print("ok bye")
                exit()

