import sqlite3
import config as cfg


dbfile = cfg.DB_PATH
con = sqlite3.connect(dbfile, check_same_thread=False)

cur = con.cursor()


def r_get_accounts():
    info = []
    rows = cur.execute("SELECT * FROM accounts").fetchall()
    for row in rows:
        account_id = row[0]
        params = (account_id,)
        # Calculating Balance
        transactions = cur.execute("SELECT * FROM transactions WHERE account_id = ?", params).fetchall()
        income, expenses = 0, 0
        new_bal = row[4]

        if len(transactions) > 0:
            for transaction in transactions:
                if transaction[2] == "income":
                    income += float(transaction[3])
                if transaction[2] == "expense":
                    expenses += float(transaction[3])
            new_bal = row[3] + income - expenses
        #     Returning rows
        row_dict = {"id" : account_id, "name": row[1], "category" : row[2], "current_balance" : new_bal}
        info.append(row_dict)
    return info


def r_get_transactions():
    info = []
    rows = cur.execute("SELECT * FROM transactions")
    for row in rows:
        row_dict = {"id" : row[0], "account_id": row[1], "type" : row[2], "amount" : row[3], "category" : row[4], "date" : row[6]}
        info.append(row_dict)
    return info

def w_add_transaction(account_id, transaction_type, amount, category, date):
    params = (account_id, transaction_type, amount, category, date)
    if float(amount) > 0:
        try:
            cur.execute("INSERT INTO transactions (account_id, type, amount, category, date) VALUES (?, ?, ?, ?, ?)", params)
            con.commit()
            return True
        except Exception as e:
            print(e)
            return False
    else:
        return False