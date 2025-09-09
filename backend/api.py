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