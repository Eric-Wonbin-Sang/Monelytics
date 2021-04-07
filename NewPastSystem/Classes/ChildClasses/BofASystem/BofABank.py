from NewPastSystem.Classes.ParentClasses import Bank
from NewPastSystem.Classes.ChildClasses.BofASystem import BofAParser, BofADebitStatement, BofACreditStatement


class BofABank(Bank.Bank):

    def __init__(self, **kwargs):

        type_to_statement_class_dict = {
            "debit": BofADebitStatement.BofADebitStatement,
            "credit": BofACreditStatement.BofACreditStatement
        }
        super().__init__(type_to_statement_class_dict=type_to_statement_class_dict, **kwargs)

    def update_accounts(self):
        parser = BofAParser.BofAParser(parent_bank=self, cookies_path=None)
        parser.update_statements()
