import os

from NewPastSystem.Classes.ParentClasses import Bank, SuperStatement
from NewPastSystem.Classes.ChildClasses.BofASystem import BofAParser, BofADebitStatement, BofACreditStatement


class BofABank(Bank.Bank):

    login_url = "https://www.bankofamerica.com/"
    auth_url = "https://secure.bankofamerica.com/login/sign-in/entry/signOnV2.go"

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        if not True:
            self.update_accounts()

        self.update_super_statements()

    def update_accounts(self):
        bofa_parser = BofAParser.BofAParser(bofa_bank=self, cookies_path=None)
        bofa_parser.update_statements()

    def update_super_statements(self):
        for account in self.account_list:
            print("--------------------------------------------------------")
            print("Account {}:".format(account.name))
            statement_list = []
            for path in os.listdir(account.statement_source_files_path):
                file_path = account.statement_source_files_path + "/" + path
                print("\tReading {}".format(file_path))
                if account.type == "debit":
                    statement_list.append(BofADebitStatement.BofADebitStatement(file_path=file_path))
                elif account.type == "credit":
                    statement_list.append(BofACreditStatement.BofACreditStatement(file_path=file_path))
                else:
                    print("UNKNOWN ACCOUNT TYPE {}".format(account.type))

            super_statement = SuperStatement.SuperStatement(statement_list=statement_list)
            if account.type == "credit":
                super_statement.update_running_total(account.curr_balance)

            print(super_statement, "\n")

    # def __str__(self):
    #     return "BofA Bank - type: {}\n\towner: {}\n\tusername: {}\n\tpassword: {}".format(
    #         self.type,
    #         self.owner,
    #         self.username,
    #         "*" * len(self.password)
    #     )
