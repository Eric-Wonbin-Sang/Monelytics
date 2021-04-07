import os

from NewPastSystem.Classes.ParentClasses import Bank, SuperStatement
from NewPastSystem.Classes.ChildClasses.VenmoSystem import VenmoParser, VenmoStatement

from General import Functions, Constants


class VenmoBank(Bank.Bank):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        if Constants.do_download:
            self.update_accounts()

        self.update_super_statements()

    def update_accounts(self):
        parser = VenmoParser.VenmoParser(parent_bank=self, cookies_path=None)
        parser.update_statements()

    def update_super_statements(self):
        for account in self.account_list:
            # print("--------------------------------------------------------")
            # print("Account {}:".format(account.name))
            statement_list = []
            for path in os.listdir(account.statement_source_files_path):
                file_path = account.statement_source_files_path + "/" + path
                # print("\tReading {}".format(file_path))
                statement_list.append(VenmoStatement.VenmoStatement(file_path=file_path))

            super_statement = SuperStatement.SuperStatement(
                statement_list=statement_list,
                super_statement_path=account.super_statement_path
            )
            # print(Functions.tab_str(Functions.df_to_str(super_statement.super_statement_df), 2))
