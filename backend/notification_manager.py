import sqlite3
from datetime import datetime
import config as cfg
import logging


dbfile = cfg.get("db_path", "db/ledgerly.db")


def check_bal(accounts):
    if accounts is None or len(accounts) == 0:
        return

    if bool(cfg.get("notifications.enable_low_balance_alerts", True)) is False:
        return

    threshold = float(cfg.get("notifications.low_balance_threshold", 50))

    con = sqlite3.connect(dbfile, check_same_thread=False)
    cur = con.cursor()

    for account in accounts:
        account_id = account['id']
        account_name = account['name']
        balance = float(account['current_balance'])

        if balance < threshold:
            count = cur.execute(
                "SELECT COUNT(*) FROM notifications WHERE type = 'low_balance' AND account_id = ? AND resolved = 0",
                (account_id,)
            ).fetchone()

            if count[0] == 0:
                params = (
                    'low_balance',
                    f"Low balance alert: Your account '{account_name}' balance is ${balance:.2f}, which is below the threshold of ${threshold:.2f}.",
                    account_id,
                    0
                )
                cur.execute(
                    "INSERT INTO notifications (type, message, account_id, status, created_at, resolved) VALUES (?, ?, ?, 'unread', date(), ?)",
                    params
                )
                con.commit()
                logging.info(f"Low balance notification created for account {account_name} with balance ${balance:.2f}")

        else:
            cur.execute(
                "UPDATE notifications SET resolved = 1 WHERE type = 'low_balance' AND account_id = ? AND resolved = 0",
                (account_id,)
            )
            con.commit()

    con.close()