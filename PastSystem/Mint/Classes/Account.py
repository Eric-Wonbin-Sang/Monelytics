
class Account:

    def __init__(self, account_dict):

        self.account_dict = account_dict

        self.account_name = self.account_dict["accountName"]
        self.parent_bank_str, self.type, self.account_number = self.account_name.split()
        # self.account_number = self.account_dict["yodleeAccountNumberLast4"]

        self.is_active = self.account_dict["isActive"]

    def get_save_filename(self):
        return self.account_name + ".p"

    def __str__(self):
        return "".join(
            [
                "ACCOUNT",
                str(self.account_dict)
            ]
        )
