
class Transaction:

    def __init__(self, **kwargs):

        self.amount = kwargs.get("amount")
        self.datetime = kwargs.get("datetime")
        self.account = kwargs.get("account")
        self.balance = kwargs.get("balance")
        self.description = kwargs.get("description")
        self.tag_list = kwargs.get("tag_list")

    def __str__(self):

        return "Date: {} \tAmt: {} \tAcc: {} \t Desc: {} \t Tags: {}".format(
            self.datetime,
            self.amount,
            self.account,
            self.description,
            self.tag_list
        )


def are_transactions_the_same(transaction_0, transaction_1):
    if transaction_0.amount == transaction_1.amount and \
            transaction_0.datetime == transaction_1.datetime and \
            transaction_0.account == transaction_1.account and \
            transaction_0.description == transaction_1.description and \
            transaction_0.tag_list == transaction_1.tag_list:
        return True
    return False


def is_transaction_in_list(curr_transaction, transaction_list):
    for transaction in transaction_list:
        if are_transactions_the_same(curr_transaction, transaction):
            return True
    return False
