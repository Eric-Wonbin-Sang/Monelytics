import os

from General import Functions


class Account:

    def __init__(self, parent_bank, dir_name, is_temp=False, **kwargs):

        self.parent_bank = parent_bank
        self.dir_name = dir_name if dir_name else self.get_dir_name()
        self.dir_path = self.parent_bank.accounts_dir_path + "/" + self.dir_name

        self.name = kwargs.get("name")
        self.nickname = kwargs.get("nickname")
        self.type = kwargs.get("type")
        self.specific_type = kwargs.get("specific_type")
        self.account_number = kwargs.get("account_number")
        self.routing_number_dict = kwargs.get("routing_number_dict")
        self.opened_date = kwargs.get("opened_date")
        self.account_url = kwargs.get("account_url")
        self.account_dict = self.get_account_dict()
        self.account_json_path = self.dir_path + "/" + "account.json"

        if dir_name is None and not is_temp:
            # print("Initializing account:", self.name)
            self.initialize_account_structure()
        else:
            # print("Found account:", self.name)
            pass

    def get_dir_name(self):
        count = 1
        num_list = []
        for account_dir in os.listdir(self.parent_bank.accounts_dir_path):
            num_list.append(int(account_dir.split("_")[-1]))
        while True:
            if count not in num_list:
                return "account_{}".format(str(count).rjust(2, "0"))
            count += 1

    def get_account_dict(self):
        return {
            "name": self.name,
            "nickname": self.nickname,
            "type": self.type,
            "specific_type": self.specific_type,
            "account_number": self.account_number,
            "routing_number_dict": self.routing_number_dict,
            # "opened_date": self.opened_date,
            "account_url": self.account_url
        }

    def initialize_account_structure(self):
        os.mkdir(self.parent_bank.accounts_dir_path + "/" + self.dir_name)
        print(self.account_dict)
        print("----------")
        Functions.dict_to_json(self.account_dict, self.account_json_path)

    def __str__(self):
        return "Account - child of {}_id{}\n\t{}\n\t{}\n\t{}\n\t{}\n\t{}\n\t{}\n\t{}".format(
            self.parent_bank.type,
            self.name,
            self.nickname,
            self.type,
            self.specific_type,
            self.account_number,
            self.routing_number_dict,
            self.opened_date,
            self.account_url
        )
