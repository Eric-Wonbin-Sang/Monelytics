import os

from NewPastSystem.Classes.ParentClasses import Bank, SuperStatement, StatementCleaner
from NewPastSystem.Classes.ChildClasses.BofASystem import BofAParser, BofADebitStatement, BofACreditStatement

from General import Functions, Constants


class BofABank(Bank.Bank):

    login_url = "https://www.bankofamerica.com/"
    auth_url = "https://secure.bankofamerica.com/login/sign-in/entry/signOnV2.go"

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        if Constants.do_download:
            self.update_accounts()

        self.update_super_statements()

        for account in self.account_list:
            StatementCleaner.StatementCleaner(
                account,
                type_to_statement_class_dict={
                    "debit": BofADebitStatement.BofADebitStatement,
                    "credit": BofACreditStatement.BofACreditStatement
                }
            )

    def update_accounts(self):
        bofa_parser = BofAParser.BofAParser(parent_bank=self, cookies_path=None)
        bofa_parser.update_statements()

    def update_super_statements(self):
        for account in self.account_list:
            # print("--------------------------------------------------------")
            # print("Account {}:".format(account.name))
            statement_list = []
            for path in os.listdir(account.statement_source_files_path):
                file_path = account.statement_source_files_path + "/" + path
                # print("\tReading {}".format(file_path))
                if account.type == "debit":
                    statement_list.append(BofADebitStatement.BofADebitStatement(parent_account=account, file_path=file_path))
                elif account.type == "credit":
                    statement_list.append(BofACreditStatement.BofACreditStatement(parent_account=account, file_path=file_path))
                else:
                    print("UNKNOWN ACCOUNT TYPE {}".format(account.type))

            if account.type == "credit":
                SuperStatement.SuperStatement(
                    statement_list=statement_list,
                    super_statement_path=account.super_statement_path,
                    is_credit=True,
                    starting_balance=account.curr_balance
                )
            else:
                SuperStatement.SuperStatement(
                    statement_list=statement_list,
                    super_statement_path=account.super_statement_path
                )

            # print(Functions.tab_str(Functions.df_to_str(super_statement.super_statement_df), 2))
