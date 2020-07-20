
class Day:

    def __init__(self, **kwargs):

        self.time_spec = kwargs.get("time_spec")        # datetime date object
        self.transaction_list = kwargs.get("transaction_list")

    def add_transaction(self, transaction):
        self.transaction_list.append(transaction)

    def __str__(self):
        return "T: {} \t transaction count: {}".format(self.time_spec, len(self.transaction_list))
