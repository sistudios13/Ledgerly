import sqlite3
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
import config as cfg


dbfile = cfg.DB_PATH



def r_get_accounts():
    con = sqlite3.connect(dbfile, check_same_thread=False)
    cur = con.cursor()

    info = []
    rows = cur.execute("SELECT * FROM accounts").fetchall()
    today = datetime.today()

    for row in rows:
        account_id = row[0]
        params = (account_id,)
        transactions = cur.execute("SELECT * FROM transactions WHERE account_id = ?", params).fetchall()

        income, expenses = 0, 0
        new_bal = row[4]

        for transaction in transactions:
            tx_type = transaction[2]
            amount = float(transaction[3])
            is_recurring = transaction[7]
            recurrence_rule = transaction[8]
            date_str = transaction[6]
            end_date_str = transaction[9]
            date = datetime.strptime(date_str, "%m/%d/%Y")
            effective_end = today
            if end_date_str:
                end_date = datetime.strptime(end_date_str, "%m/%d/%Y")
                effective_end = min(today, end_date)


            occurrences = 1

            if not is_recurring and date > today:
                occurrences = 0

            if is_recurring:
                if recurrence_rule == "daily":
                    occurrences = (effective_end - date).days + 1
                elif recurrence_rule == "weekly":
                    occurrences = ((effective_end - date).days // 7) + 1
                elif recurrence_rule == "biweekly":
                    occurrences = ((effective_end - date).days // 14) + 1
                elif recurrence_rule == "monthly":
                    delta = relativedelta(effective_end, date)
                    occurrences = delta.years * 12 + delta.months + 1
                elif recurrence_rule == "yearly":
                    delta = relativedelta(effective_end, date)
                    occurrences = delta.years + 1
                if date > today:
                    occurrences = 0



            total_amount = amount * occurrences

            # Apply to balance
            if tx_type == "income":
                income += total_amount
            elif tx_type == "expense":
                expenses += total_amount

        new_bal = row[3] + income - expenses

        row_dict = {
            "id": account_id,
            "name": row[1],
            "category": row[2],
            "current_balance": new_bal
        }
        info.append(row_dict)

    return info

def r_get_transactions():
    con = sqlite3.connect(dbfile, check_same_thread=False)
    cur = con.cursor()

    info = []
    rows = cur.execute("SELECT * FROM transactions ORDER BY date DESC LIMIT 49999 OFFSET 0").fetchall()
    today = datetime.today().date()

    for row in rows:
        transaction_id = row[0]
        account_id = row[1]
        t_type = row[2]
        base_amount = float(row[3])
        category = row[4]
        note = row[5]
        txn_date = row[6]

        date = datetime.strptime(txn_date, "%m/%d/%Y").date()

        is_recurring = row[7]
        recurrence_rule = row[8]  # daily, weekly, monthly
        end_date = row[9]

        if end_date:
            end_date = datetime.strptime(end_date, "%m/%d/%Y").date()

        total_amount = base_amount



        if is_recurring == 1 and recurrence_rule:
            effective_end = end_date if end_date else today

            if effective_end > today:
                effective_end = today

            if effective_end < date:
                occurrences = 0

            if date > today:
                occurrences = 0

            else:
                if recurrence_rule == "daily":
                    occurrences = (effective_end - date).days + 1

                elif recurrence_rule == "weekly":
                    occurrences = ((effective_end - date).days // 7) + 1

                elif recurrence_rule == "biweekly":
                    occurrences = ((effective_end - date).days // 14) + 1

                elif recurrence_rule == "monthly":
                    delta = relativedelta(effective_end, date)
                    occurrences = delta.years * 12 + delta.months + 1

                elif recurrence_rule == "yearly":
                    delta = relativedelta(effective_end, date)
                    occurrences = delta.years + 1

                else:
                    occurrences = 1
            total_amount = base_amount * occurrences


        row_dict = {
            "id": transaction_id,
            "account_id": account_id,
            "type": t_type,
            "amount": total_amount,
            "recurring_amount": base_amount,
            "category": category,
            "note": note,
            "date": str(txn_date),
            "is_recurring": bool(is_recurring),
            "recurrence_rule": recurrence_rule,
            "end_date": row[9]
        }
        info.append(row_dict)

    return info

def w_add_transaction(account_id, transaction_type, amount, category, date):
    con = sqlite3.connect(dbfile, check_same_thread=False)
    cur = con.cursor()

    params = (account_id, transaction_type, amount, category, date)
    if float(amount) > 0 and date is not None:
        try:
            cur.execute("INSERT INTO transactions (account_id, type, amount, category, date) VALUES (?, ?, ?, ?, ?)", params)
            con.commit()
            return True
        except Exception as e:
            print(e)
            return False
    else:
        print("Error: Amount less than 0")
        return False

def w_add_long_transaction(account_id, transaction_type, amount, category, note, date, is_recurring, recurrence_rule, end_date):
    con = sqlite3.connect(dbfile, check_same_thread=False)
    cur = con.cursor()

    params = (account_id, transaction_type, amount, category, note, date)
    if float(amount) > 0 and not is_recurring and date is not None:
        try:
            cur.execute("INSERT INTO transactions (account_id, type, amount, category, note, date) VALUES (?, ?, ?, ?, ?, ?)",
                        params)
            con.commit()
            return True
        except Exception as e:
            print(e)
            return False
    if float(amount) > 0 and is_recurring and date is not None and recurrence_rule is not None:
        params = (account_id, transaction_type, amount, category, note, date, is_recurring, recurrence_rule, end_date)
        if date == "":
            print("Error: No date")
            return False
        if recurrence_rule == "na":
            print("Error: No recurrence rule")
            return False

        date = datetime.strptime(date, "%m/%d/%Y").date()
        if end_date:
            end_date = datetime.strptime(end_date, "%m/%d/%Y").date()
            if end_date < date:
                print("Error: End date before date")
                return False
        try:
            cur.execute("INSERT INTO transactions (account_id, type, amount, category, note, date, is_recurring, recurrence_rule, end_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        params)
            con.commit()
            return True
        except Exception as e:
            print(e)
            return False




    else:
        print("Error: Invalid entry, check recurrence, amount, date or end date")
        return False

def w_add_account(name, category, initial_balance):
    con = sqlite3.connect(dbfile, check_same_thread=False)
    cur = con.cursor()

    default_currency = cfg.DEFAULT_CURRENCY
    params = (name, category, initial_balance, initial_balance, default_currency)
    if len(name) > 0 and len(category) > 0:
        try:
            cur.execute(
                "INSERT INTO accounts (name, type, starting_balance, current_balance, currency) VALUES (?, ?, ?, ?, ?)",
                params)
            con.commit()
            return True
        except Exception as e:
            print(e)
            return False
    else:
        print("Error: No name or category")
        return False
    

def w_delete_account(account_id):
    con = sqlite3.connect(dbfile, check_same_thread=False)
    cur = con.cursor()

    params = (account_id,)
    if account_id:
        try:
            cur.execute(
                "DELETE FROM accounts WHERE id = ?",
                params)
            cur.execute(
                "DELETE FROM transactions WHERE account_id = ?",
                params)
            con.commit()
            return True
        except Exception as e:
            print(e)
            return False
    else:
        print("Error: No account id given")
        return False

def w_edit_account(account_id, name, category):
    con = sqlite3.connect(dbfile, check_same_thread=False)
    cur = con.cursor()
    params = (name, category, account_id)
    if len(name) > 0 and len(category) > 0:
        try:
            cur.execute(
                "UPDATE accounts SET name = ?, type = ? WHERE id = ?",
                params)
            con.commit()
            return True
        except Exception as e:
            print(e)
            return False
    else:
        print("Error: No name or category")
        return False

def expand_recurring(row):
    today = date.today()
    txs = []
    (
        id, acc_id, t_type, amount, category, note, tx_date,
        is_recurring, recurrence_rule, end_date
    ) = row

    base_date = datetime.strptime(tx_date, "%m/%d/%Y").date()
    effective_end = datetime.strptime(end_date, "%m/%d/%Y").date() if end_date else today
    effective_end = min(effective_end, today)

    # Non-recurring
    if not is_recurring or recurrence_rule is None:
        txs.append((base_date, t_type, amount))
        return txs

    # Recurring
    current = base_date
    while current <= effective_end:
        txs.append((current, t_type, amount))
        if recurrence_rule == "daily":
            current += timedelta(days=1)
        elif recurrence_rule == "weekly":
            current += timedelta(weeks=1)
        elif recurrence_rule == "biweekly":
            current += timedelta(weeks=2)
        elif recurrence_rule == "monthly":
            current += relativedelta(months=1)
        elif recurrence_rule == "yearly":
            current += relativedelta(years=1)
        else:
            break
    return txs

def w_delete_transaction(transaction_id):
    con = sqlite3.connect(dbfile, check_same_thread=False)
    cur = con.cursor()

    params = (transaction_id,)
    if transaction_id:
        try:
            cur.execute(
                "DELETE FROM transactions WHERE id = ?",
                params)
            con.commit()
            return True
        except Exception as e:
            print(e)
            return False
    else:
        print("Error: No transaction id given")
        return False



def r_get_balance_over_time(account_id):
    con = sqlite3.connect(dbfile, check_same_thread=False)
    cur = con.cursor()

    today = date.today()
    daily_balances = {}

    # Build query
    sql = "SELECT * FROM transactions"
    params = ()
    if account_id:
        sql += " WHERE account_id = ?"
        params = (account_id,)
    sql += " ORDER BY date ASC"
    rows = cur.execute(sql, params).fetchall()


    expanded = []
    for row in rows:
        expanded.extend(expand_recurring(row))

    # Sort by date
    expanded.sort(key=lambda x: x[0])

    # Starting balance
    balance = cur.execute("SELECT starting_balance FROM accounts WHERE id = ?", (account_id,)).fetchone()[0]


    for d, t_type, amount in expanded:
        if t_type == "income":
            balance += amount
        elif t_type == "expense":
            balance -= amount


        daily_balances[d] = balance

    # Convert to sorted list of dicts
    info = [{"date": d.strftime("%m-%d-%Y"), "value": v} for d, v in sorted(daily_balances.items())]

    return info


def r_get_total_by_category(account_id, t_type):
    con = sqlite3.connect(dbfile, check_same_thread=False)
    cur = con.cursor()

    params = (account_id, t_type)
    rows = cur.execute("SELECT * FROM transactions WHERE account_id = ? AND type = ?", params).fetchall()

    totals = {}


    for row in rows:

        amount = expand_recurring(row)[0][2]
        category = row[4] if row[4] else "Other"

        if category not in totals:
            totals[category] = 0
        totals[category] += amount

    numbers = list(totals.values())
    labels = list(totals.keys())

    info = [numbers, labels]

    print(info)
    return info
