import os

from NewPastSystem.Classes.ParentClasses import Account

from General import Functions, Constants


class Bank:

    banks_dir = Constants.banks_dir

    def __init__(self, dir_name, **kwargs):

        self.type = kwargs.get("type")
        self.owner = kwargs.get("owner")
        self.username = kwargs.get("username")
        self.password = kwargs.get("password")
        self.bank_dict = self.get_bank_dict()

        self.dir_name = dir_name if dir_name else self.generate_dir_name()
        self.general_path = self.banks_dir + "/" + self.dir_name
        self.accounts_dir_path = self.general_path + "/" + "accounts"
        self.bank_json_path = self.general_path + "/" + "bank.json"

        if dir_name is None:
            self.initialize_bank_structure()

        self.account_list = self.get_account_list()     # these are accounts that already exist

    def get_bank_dict(self):
        return {
            "type": self.type,
            "owner": self.owner,
            "username": self.username,
            "password": self.password
        }

    def generate_dir_name(self):
        count = 1
        num_list = []
        for account_dir in os.listdir(self.banks_dir):
            if not os.path.isdir(self.banks_dir + "/" + account_dir):
                continue
            num_list.append(int(account_dir.split("_")[-1]))
        while True:
            if count not in num_list:
                return "bank_{}".format(str(count).rjust(2, "0"))
            count += 1

    def initialize_bank_structure(self):
        os.mkdir(self.general_path)
        os.mkdir(self.accounts_dir_path)
        Functions.dict_to_json(self.bank_dict, self.bank_json_path)

    def get_account_list(self):
        account_list = []
        for dir_name in os.listdir(self.accounts_dir_path):
            account_json_path = self.accounts_dir_path + "/" + dir_name + "/" + "account.json"
            account_dict = Functions.parse_json(account_json_path)
            account_list.append(
                Account.Account(
                    parent_bank=self,
                    dir_name=dir_name,
                    **account_dict
                )
            )
        return account_list

    def __str__(self):
        return "Generic Bank - type: {}\n\towner: {}\n\tusername: {}\n\tpassword: {}".format(
            self.type,
            self.owner,
            self.username,
            "*" * len(self.password)
        ) + "\n\thas {} account(s)".format(len(self.account_list))
