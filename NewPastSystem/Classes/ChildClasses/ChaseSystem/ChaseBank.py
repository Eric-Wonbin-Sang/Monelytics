import os

from NewPastSystem.Classes.ParentClasses import Bank, SuperStatement
from NewPastSystem.Classes.ChildClasses.ChaseSystem import ChaseParser, ChaseDebitStatement, ChaseCreditStatement

from General import Functions, Constants


class ChaseBank(Bank.Bank):

    def __init__(self, **kwargs):

        type_to_statement_class_dict = {
            "debit": ChaseDebitStatement.ChaseDebitStatement,
            "credit": ChaseCreditStatement.ChaseCreditStatement
        }
        super().__init__(type_to_statement_class_dict=type_to_statement_class_dict, **kwargs)

        if Constants.do_download:
            self.update_accounts()

        self.update_super_statements()

    def update_accounts(self):
        parser = ChaseParser.ChaseParser(parent_bank=self, cookies_path=None)
        parser.update_statements()
