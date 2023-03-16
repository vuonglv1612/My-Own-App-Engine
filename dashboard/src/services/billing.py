class BillingClient:
    def __init__(self, billing_url):
        self.billing_url = billing_url

    async def create_account(self, name: str):
        # TODO: implement this
        account_id = "account_id_123"
        return account_id

    async def delete_account(self, account_id: str):
        print("Deleting account: ", account_id)
        return True
