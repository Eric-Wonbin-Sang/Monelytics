from AccountParsers import Transaction

from General import Functions


class Account:

    def __init__(self, **kwargs):

        self.name = kwargs.get("name")
        self.id = kwargs.get("id")

        self.day_transaction_list_dict = {}

    def add_statement(self, statement):
        for day in statement.day_transaction_list_dict:
            if day in self.day_transaction_list_dict:
                for new_transaction in statement.day_transaction_list_dict[day]:
                    if not Transaction.is_transaction_in_list(new_transaction, self.day_transaction_list_dict[day]):
                        self.day_transaction_list_dict[day] += [statement.day_transaction_list_dict[day]]
            else:
                self.day_transaction_list_dict[day] = statement.day_transaction_list_dict[day]

    def __str__(self):
        ret_str = "Name: {} \tID: {}\n".format(
            self.name,
            self.id,
        )
        i = 1
        if i == 0:
            for d_i, day in enumerate(self.day_transaction_list_dict):
                if d_i != 0:
                    ret_str += "\n"
                ret_str += "Day: {}".format(day)
                for transaction in self.day_transaction_list_dict[day]:
                    ret_str += "\n\t{}".format(transaction)
            return ret_str
        else:
            for d_i, day in enumerate(self.day_transaction_list_dict):
                if d_i != 0:
                    ret_str += "\n"
                ret_str += "{} Day: {} - transaction count: {}".format(d_i, day,
                                                                       len(self.day_transaction_list_dict[day]))
            return ret_str


def find_account(name, account_list):
    for account in account_list:
        if account.name == name:
            return account
    return None
