import config as cfg
import backend.db_manager as dbm


class LedgerlyApi:
    def get_info(self):
        return {"version": cfg.APP_VERSION}

    def get_accounts(self):
        return dbm.r_get_accounts()

    def get_transactions(self):
        return dbm.r_get_transactions()

    def add_transaction(self, account_id, transaction_type, amount, category, date):
        return dbm.w_add_transaction(account_id, transaction_type, amount, category, date)

    def add_long_transaction(self, account_id, transaction_type, amount, category, note, date, is_recurring, recurrence_rule, end_date):
        return dbm.w_add_long_transaction(account_id, transaction_type, amount, category, note, date, is_recurring, recurrence_rule, end_date)

    def add_account(self, name, category, initial_balance):
        return dbm.w_add_account(name, category, initial_balance)

    def delete_account(self, a_id):
        return dbm.w_delete_account(a_id)

    def delete_transaction(self, transaction_id):
        return dbm.w_delete_transaction(transaction_id)

    def edit_account(self, account_id, name, category):
        return dbm.w_edit_account(account_id, name, category)

    def get_balance_over_time(self, account_id):
        return dbm.r_get_balance_over_time(account_id)

    def get_total_by_category(self, account_id, t_type):
        return dbm.r_get_total_by_category(account_id, t_type)