import os

from NewPastSystem.Classes.ParentClasses import Bank, SuperStatement, StatementCleaner
from NewPastSystem.Classes.ChildClasses.BofASystem import BofAParser, BofADebitStatement, BofACreditStatement
from NewPastSystem.Classes.ChildClasses.DiscoverSystem import DiscoverParser, DiscoverStatement

from General import Functions, Constants


class DiscoverBank(Bank.Bank):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        if Constants.do_download:
            self.update_accounts()

        self.update_super_statements()

        for account in self.account_list:
            StatementCleaner.StatementCleaner(
                account,
                type_to_statement_class_dict={
                    "credit": DiscoverStatement.DiscoverStatement,
                }
            )

    def update_accounts(self):
        parser = DiscoverParser.DiscoverParser(parent_bank=self, cookies_path=None)
        parser.update_statements()

    def update_super_statements(self):
        for account in self.account_list:
            # print("--------------------------------------------------------")
            # print("Account {}:".format(account.name))
            statement_list = []
            for path in os.listdir(account.statement_source_files_path):
                file_path = account.statement_source_files_path + "/" + path
                # print("\tReading {}".format(file_path))
                if account.type == "credit":
                    statement_list.append(DiscoverStatement.DiscoverStatement(parent_account=account, file_path=file_path))
                else:
                    print("UNKNOWN ACCOUNT TYPE {}".format(account.type))

            super_statement = SuperStatement.SuperStatement(
                statement_list=statement_list,
                super_statement_path=account.super_statement_path,
                is_credit=True,
                starting_balance=account.curr_balance
            )
            # print(Functions.tab_str(Functions.df_to_str(super_statement.super_statement_df), 2))
