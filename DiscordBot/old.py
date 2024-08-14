'''SELECT SUM(payments.amount) as total FROM transactions
            LEFT JOIN payments 
            ON payments.transaction_id = transactions.id
            WHERE payments.user_id_paid_by = %s
            AND transactions.user_id_paid_by = %s;'''

def balanceCalc(payer, payee):
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
    if balance > 0 :
        print(users.usersTable[int(payer)].name + " owes " + users.usersTable[int(payee)].name + " $" + str(balance))
    elif balance < 0:
        print(users.usersTable[int(payee)].name + " owes " + users.usersTable[int(payer)].name + " $" + str(-1*balance))
    else:
        print("There is no debt between " + users.usersTable[int(payee)].name + " and " + users.usersTable[int(payer)].name)
    

    db.close() 