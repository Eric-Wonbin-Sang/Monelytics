import os

from NewPastSystem.Classes.ParentClasses import Bank, SuperStatement, StatementCleaner
from NewPastSystem.Classes.ChildClasses.BofASystem import BofAParser, BofADebitStatement, BofACreditStatement

from General import Functions, Constants


class BofABank(Bank.Bank):

    login_url = "https://www.bankofamerica.com/"
    auth_url = "https://secure.bankofamerica.com/login/sign-in/entry/signOnV2.go"

    def __init__(self, **kwargs):

        type_to_statement_class_dict = {
            "debit": BofADebitStatement.BofADebitStatement,
            "credit": BofACreditStatement.BofACreditStatement
        }
        super().__init__(type_to_statement_class_dict=type_to_statement_class_dict, **kwargs)

        if Constants.do_download:
            self.update_accounts()

        self.update_super_statements()

    def update_accounts(self):
        bofa_parser = BofAParser.BofAParser(parent_bank=self, cookies_path=None)
        bofa_parser.update_statements()
