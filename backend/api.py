import config as cfg


class LedgerlyApi:
    def get_info(self):
        return {"version": cfg.APP_VERSION}

    # def get_accounts(self):
    #     # Placeholder for actual account retrieval logic
    #     return [{"id": 1, "name": "Checking"}, {"id": 2, "name": "Savings"}]

    # def get_transactions(self):
    #     # Placeholder for actual transaction retrieval logic
    #     return [{"id": 1, "amount": 100, "account_id": 1}, {"id": 2, "amount": -50, "account_id": 2}]