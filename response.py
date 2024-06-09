def handle_response(command) -> str:
    message = command.lower()

    if message == "hbot":
        return 'Hi,' \
        '\nPlease select from the following options:\n' \
        '\n1. Enter new expense\n2. '\
        'View current household dues\n3. ' \
        'Display monthly payment breakdown\n4. ' \
        'Exit Program.\n\n' \
        'Option Selected: '