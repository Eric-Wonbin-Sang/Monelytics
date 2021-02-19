
class Bank:

    def __init__(self, **kwargs):

        self.type = kwargs.get("bank_type")
        self.username = kwargs.get("username")
        self.password = kwargs.get("password")

    def __str__(self):
        return "Generic Bank - type: {}\n\tusername: {}\n\tpassword: {}".format(
            self.type,
            self.username,
            "*" * len(self.password)
        )


def get_bank_list(bank_dict_list):
    bank_list = []
    for bank_dict in bank_dict_list:
        bank_type = bank_dict.get("bank_type")
        if bank_type == "Bank of America":
            bank_list.append(Bank(**bank_dict))
        elif bank_type == "Discover":
            bank_list.append(Bank(**bank_dict))
        elif bank_type == "Chase":
            bank_list.append(Bank(**bank_dict))
        elif bank_type == "Venmo":
            bank_list.append(Bank(**bank_dict))
        elif bank_type == "Mint":
            bank_list.append(Bank(**bank_dict))
        else:
            print("unknown bank type:", bank_type)
    return bank_list
