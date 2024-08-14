import transactions
import users
import charges
import payments
import database
from datetime import datetime
from discord.ext import commands
from bot_instance import bot

@bot.command()
async def seeBalance(ctx, payer, payee, option):
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
            await ctx.send(f"An error occurred while fetching transactions: {e}")
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
            await ctx.send(f"An error occurred while fetching payments: {e}")
            res2 = 0

        balance = res - res2

        if option == 1:
            await ctx.send(f"To {users.showUser(int(payee)):<5}\t${balance:.2f}")

        return balance

    except Exception as e:
        await ctx.send(f"An unexpected error occurred: {e}")
        return 0

    finally:
        db.close()


@bot.command()
async def add_user(ctx):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    try:
        await ctx.send("Enter the name: ")
        name = (await bot.wait_for('message', check=check)).content.strip()
        if not name:
            raise ValueError("Name cannot be empty.")
        nameSet = users.displayUsers(1)
        if name in nameSet:
            raise ValueError("Name already taken. Try something else")

        await ctx.send("Enter the phone number: ")
        phone_number = (await bot.wait_for('message', check=check)).content
        
        if not phone_number.isdigit():
            raise ValueError("Phone number must contain only digits.")
        if len(phone_number) < 7 or len(phone_number) > 15:
            raise ValueError("Phone number must be between 7 and 15 digits long.")

        await ctx.send("Enter the email: ")
        email = (await bot.wait_for('message', check=check)).content

        if "@" not in email or "." not in email:
            raise ValueError("Email must be a valid email address.")

        users.User.create(None, name, phone_number, email)
        await ctx.send("User created successfully!")

    except ValueError as e:
        await ctx.send(f"Input error: {e}")

@bot.command()
async def new_expense(ctx):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    try:
        await ctx.send("The expense falls under which category: ")
        categories, cat_set = transactions.displayCategories()
        await ctx.send(categories)  # Send the categories to the Discord channel
        category_msg = await bot.wait_for('message', check=check)
        transaction_category_id = category_msg.content.strip()
        if not transaction_category_id.isdigit():
            await ctx.send("Category ID must be a number.")
            return
        if transaction_category_id not in cat_set:
            await ctx.send("Category ID does not exist.")
            return
        transaction_category_id = int(transaction_category_id)

        await ctx.send("Paid by: ")
        await ctx.send(users.displayUsers())
        paid_by_msg = await bot.wait_for('message', check=check)
        user_id_paid_by = paid_by_msg.content.strip()
        if not user_id_paid_by.isdigit():
            await ctx.send("User ID must be a number.")
            return
        user_id_paid_by = int(user_id_paid_by)
        if user_id_paid_by not in users.usersTable:
            await ctx.send("User ID does not exist.")
            return
        await ctx.send(f"Paid by {users.showUser(user_id_paid_by)}")

        await ctx.send("How much: ")
        amount_msg = await bot.wait_for('message', check=check)
        try:
            amount = float(amount_msg.content)
            if amount <= 0:
                await ctx.send("Amount must be positive.")
                return
        except ValueError:
            await ctx.send("Amount must be a valid number.")
            return
        
        await ctx.send("Source of purchase: ")
        source_msg = await bot.wait_for('message', check=check)
        source = source_msg.content.strip()
        if not source:
            await ctx.send("Source cannot be empty.")
            return

        users_paying = []
        count = 0
        while True:
            await ctx.send("Who needs to pay: ")
            await ctx.send(users.displayUsers())
            user_msg = await bot.wait_for('message', check=check)
            hold = user_msg.content.strip()
            if not hold.isdigit() or int(hold) not in users.usersTable:
                await ctx.send("Invalid user ID. Please enter a valid number.")
                continue
            user_id = int(hold)
            await ctx.send(f"Confirm charge to {users.showUser(user_id)}? (y/n)")
            confirm_msg = await bot.wait_for('message', check=check)
            if confirm_msg.content.lower() == "y":
                users_paying.append(user_id)
                count += 1
            if count > 0:
                await ctx.send("Charge another user? (y/n)")
                again_msg = await bot.wait_for('message', check=check)
                if again_msg.content.lower() == "n":
                    break

        await ctx.send("Description: ")
        description_msg = await bot.wait_for('message', check=check)
        description = description_msg.content.strip()
        if not description:
            await ctx.send("Description cannot be empty.")
            return
        
        date = await date_input(ctx, check, "Date of purchase (YYYY-MM-DD) or type 'today': ")

        await ctx.send("Created by: ")
        await ctx.send(users.displayUsers())
        created_by_msg = await bot.wait_for('message', check=check)
        created_by = created_by_msg.content.strip()
        if not created_by.isdigit() or int(created_by) not in users.usersTable:
            await ctx.send("User ID must be a valid number in the user list.")
            return
        created_by = int(created_by)

        split_to_users = len(users_paying) + 1
        split = amount / split_to_users

        await ctx.send(f"Confirm transaction:\n{users.showUser(user_id_paid_by)} paid ${amount:.2f} for {description}")
        await ctx.send(f"The following user(s) will be charged ${split:.2f} each:")
        for user in users_paying:
            await ctx.send(users.showUser(int(user)))
        
        await ctx.send("Confirm? (y/n)")
        confirm_msg = await bot.wait_for('message', check=check)
        if confirm_msg.content.lower() == "n":
            await ctx.send("Cancel transaction? (y/n)")
            cancel_msg = await bot.wait_for('message', check=check)
            if cancel_msg.content.lower() == "y":
                await ctx.send("Transaction cancelled.")
                return

        new_trans = transactions.Transactions.create(None, transaction_category_id, user_id_paid_by, amount, source, split_to_users, description, date, None, None, created_by)
        
        for user in users_paying:
            charges.Charges.create(None, new_trans.id, user, split, created_by, None, None, None)

        await ctx.send("Transaction created!")

    except ValueError as e:
        await ctx.send(f"Input error: {e}")
    except Exception as e:
        await ctx.send(f"An unexpected error occurred: {e}")

@bot.command()
async def date_input(ctx, check, prompt, auto_date_keyword="today"):
    while True:
        await ctx.send(prompt)
        date_msg = await bot.wait_for('message', check=check)
        date_input = date_msg.content.strip()
        if date_input.lower() == auto_date_keyword:
            return datetime.today().strftime('%Y-%m-%d')
        try:
            date_obj = datetime.strptime(date_input, '%Y-%m-%d')
            return date_obj.strftime('%Y-%m-%d')
        except ValueError:
            await ctx.send("Invalid date format. Please enter the date in YYYY-MM-DD format or type 'today' for the current date.")
    
@bot.command()
async def display_dues(ctx):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    try:
        await ctx.send("Whose dues would you like to see?\nPlease select from the following options:\n")
        await ctx.send(users.displayUsers())
        user_dues = (await bot.wait_for('message', check=check)).content
        if not user_dues.isdigit() or int(user_dues) not in users.usersTable:
            raise ValueError("Invalid user ID selected.")
        user_dues = int(user_dues)
        
        await ctx.send(users.showUser(user_dues) + "'s Balance")
        await ctx.send("----------------------------")
        
        total = 0
        for i in users.usersTable:
            if i == user_dues:
                continue
            total += await seeBalance(ctx, user_dues, i, 1)
        
        await ctx.send("\nTotal Balance: $" + f"{total:.2f}")
        await ctx.send("----------------------------")
    
    except ValueError as e:
        await ctx.send(f"Input error: {e}")


   
@bot.command()
async def make_payment(ctx):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        await ctx.send("Who is making the payment?")
        await ctx.send(users.displayUsers())
        payer_msg = await bot.wait_for('message', check=check)
        currently_paying = payer_msg.content.strip()
        if not currently_paying.isdigit() or int(currently_paying) not in users.usersTable:
            await ctx.send("Invalid user ID for who is making the payment.")
            return
        currently_paying = int(currently_paying)

        await ctx.send("Who is the payment to? ")
        payee_msg = await bot.wait_for('message', check=check)
        being_paid = payee_msg.content.strip()
        if not being_paid.isdigit() or int(being_paid) not in users.usersTable:
            await ctx.send("Invalid user ID for who is being paid.")
            return
        being_paid = int(being_paid)

        balance = await seeBalance(ctx, currently_paying, being_paid, 2)

        if balance > 0:
            await ctx.send(f"{users.showUser(currently_paying)} owes {users.showUser(being_paid)} ${balance:.2f}")
        elif balance < 0:
            await ctx.send(f"{users.showUser(being_paid)} owes {users.showUser(currently_paying)} ${-1 * balance:.2f}")
        else:
            await ctx.send(f"There is no debt between {users.showUser(being_paid)} and {users.showUser(currently_paying)}")
            await ctx.send("Would you like to continue with the payment? (y/n)")
            cont_msg = await bot.wait_for('message', check=check)
            if cont_msg.content.strip().lower() == "n":
                return

        await ctx.send("Is the payment specific to one transaction? (y/n)")
        specific_msg = await bot.wait_for('message', check=check)
        specific = specific_msg.content.strip().lower()

        transaction_id = None
        if specific == "y":
            tSet = transactions.displaySpecifiedTransactions(currently_paying, being_paid)
            if tSet:
                await ctx.send("Select from the following transactions: ")
                await ctx.send(tSet[0])
                trans_msg = await bot.wait_for('message', check=check)
                transaction_id = trans_msg.content.strip()
                print(tSet[1])
                if not transaction_id.isdigit() or int(transaction_id) not in tSet[1]:
                    await ctx.send("Invalid transaction ID.")
                    return
            else:
                await ctx.send(f"There are no transactions where {users.showUser(currently_paying)} owes {users.showUser(being_paid)}")
                await ctx.send("Would you like to continue with the payment? (y/n)")
                cont_msg = await bot.wait_for('message', check=check)
                if cont_msg.content.strip().lower() == "n":
                    return
                transaction_id = None

        await ctx.send("Payment method: ")
        method_msg = await bot.wait_for('message', check=check)
        method = method_msg.content.strip()
        if not method:
            await ctx.send("Payment method cannot be empty.")
            return

        await ctx.send("Payment amount: ")
        amount_msg = await bot.wait_for('message', check=check)
        try:
            amount = float(amount_msg.content.strip())
            if amount <= 0:
                await ctx.send("Payment amount must be positive.")
                return
        except ValueError:
            await ctx.send("Payment amount must be a valid number.")
            return

        date = await date_input(ctx, check, "Date of payment (YYYY-MM-DD) or type 'today': ")

        await ctx.send("Created by: ")
        await ctx.send(users.displayUsers())
        created_by_msg = await bot.wait_for('message', check=check)
        created_by = created_by_msg.content.strip()
        if not created_by.isdigit() or int(created_by) not in users.usersTable:
            await ctx.send("Invalid user ID for created by.")
            return
        created_by = int(created_by)

        payments.Payments.create(None, transaction_id, currently_paying, being_paid, method, amount, date, created_by, None)
        await ctx.send("Payment created successfully!")

    except ValueError as e:
        await ctx.send(f"Input error: {e}")
    except Exception as e:
        await ctx.send(f"An unexpected error occurred: {e}")

@bot.command()
async def displayCharges(ctx):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        await ctx.send("Whose dues would you like to see?\nPlease select from the following options:\n")
        await ctx.send(users.displayUsers())
        dues_msg = await bot.wait_for('message', check=check)
        user_dues = dues_msg.content.strip()
        if not user_dues.isdigit() or int(user_dues) not in users.usersTable:
            await ctx.send("Invalid user ID selected.")
            return
        user_dues = int(user_dues)

        await ctx.send(f"Dues between {users.showUser(user_dues)} and who?\nPlease select from the following options:\n")
        await ctx.send(users.displayUsers())
        specify_user_msg = await bot.wait_for('message', check=check)
        specify_user = specify_user_msg.content.strip()
        if not specify_user.isdigit() or int(specify_user) not in users.usersTable:
            await ctx.send("Invalid user ID selected.")
            return
        specify_user = int(specify_user)

        await ctx.send(charges.dues(user_dues, specify_user))

    except ValueError as e:
        await ctx.send(f"Input error: {e}")
    except Exception as e:
        await ctx.send(f"An unexpected error occurred: {e}")

@bot.command()
async def displayPayments(ctx):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        await ctx.send("Whose payments would you like to see?\nPlease select from the following options:\n")
        await ctx.send(users.displayUsers())
        payments_msg = await bot.wait_for('message', check=check)
        user_paid = payments_msg.content.strip()
        if not user_paid.isdigit() or int(user_paid) not in users.usersTable:
            await ctx.send("Invalid user ID selected.")
            return
        user_paid = int(user_paid)

        await ctx.send(f"Payments to who?\nPlease select from the following options:\n")
        await ctx.send(users.displayUsers())
        specify_user_msg = await bot.wait_for('message', check=check)
        specify_user = specify_user_msg.content.strip()
        if not specify_user.isdigit() or int(specify_user) not in users.usersTable:
            await ctx.send("Invalid user ID selected.")
            return
        specify_user = int(specify_user)

        await ctx.send(payments.paid(user_paid, specify_user))

    except ValueError as e:
        await ctx.send(f"Input error: {e}")
    except Exception as e:
        await ctx.send(f"An unexpected error occurred: {e}")

@bot.command()
async def start(ctx):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    while True:
        await ctx.send('Hi,' \
                '\nPlease select from the following options:\n\n' \
                '1. Enter new expense\n'\
                '2. View current household dues\n' \
                '3. Make payment\n' \
                '4. Add User\n' \
                '5. View charges\n' \
                '6. View payments\n' \
                '7. Exit Program\n\n' \
                'Option Selected: ')
        command = (await bot.wait_for('message', check=check)).content.strip()
        if command != "4" and command != "7" and len(users.usersTable) < 2: 
            await ctx.send("Enter at least two users before using these features!")
            continue

        match command:
            case "1":
                await new_expense(ctx)
            case "2":
                await display_dues(ctx)
            case "3":
                await make_payment(ctx)
            case "4":
                await add_user(ctx)
            case "5":
                await displayCharges(ctx)
            case "6":
                await displayPayments(ctx)
            case "7":
                await ctx.send("Bye!")
                break
            case _:
                await ctx.send("Invalid input, would you like to try again? (y/n)")
                retry = await bot.wait_for('message', check=check)
                if retry.content.strip().lower() != "y":
                    await ctx.send("Ok bye")
                    break

