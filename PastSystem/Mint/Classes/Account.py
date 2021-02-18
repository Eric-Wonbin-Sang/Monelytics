from General import Functions


class Account:

    def __init__(self, account_dict, complete_transaction_list):

        self.account_dict = account_dict

        self.name = self.account_dict["accountName"]
        self.parent_bank_str, self.type, self.account_number = self.name.split()

        self.is_active = self.account_dict["isActive"]

        self.transaction_list = self.get_transaction_list(complete_transaction_list)

    def get_save_filename(self):
        return self.name + ".p"

    def get_transaction_list(self, transaction_list):
        return [t for t in transaction_list if self.name == t.account_name]

    def get_x_y_lists(self):
        x_list, y_list = [], []
        rolling_sum = 0
        for transaction in self.transaction_list:
            rolling_sum += transaction.amount * (1 if transaction.is_debit else -1)
            x_list.append(transaction.date)
            y_list.append(rolling_sum)
        return x_list, y_list

    def __str__(self):
        return "{} | is_active: {} | len(t_list): {}".format(
            Functions.str_to_length(self.name, 24),
            Functions.str_to_length(self.is_active, 5, do_dots=False),
            len(self.transaction_list)
        )
