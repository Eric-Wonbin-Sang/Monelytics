import os

from NewPastSystem.Classes.ParentClasses import Bank, SuperStatement, StatementCleaner
from NewPastSystem.Classes.ChildClasses.BofASystem import BofAParser, BofADebitStatement, BofACreditStatement
from NewPastSystem.Classes.ChildClasses.DiscoverSystem import DiscoverParser, DiscoverStatement

from General import Functions, Constants


class DiscoverBank(Bank.Bank):

    def __init__(self, **kwargs):

        type_to_statement_class_dict = {
            "credit": DiscoverStatement.DiscoverStatement,
        }
        super().__init__(type_to_statement_class_dict=type_to_statement_class_dict, **kwargs)

        if Constants.do_download:
            self.update_accounts()

        self.update_super_statements()

    def update_accounts(self):
        parser = DiscoverParser.DiscoverParser(parent_bank=self, cookies_path=None)
        parser.update_statements()
