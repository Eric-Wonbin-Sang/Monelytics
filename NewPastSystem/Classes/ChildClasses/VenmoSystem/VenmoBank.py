from NewPastSystem.Classes.ParentClasses import Bank
from NewPastSystem.Classes.ChildClasses.VenmoSystem import VenmoParser, VenmoStatement


class VenmoBank(Bank.Bank):

    def __init__(self, **kwargs):

        type_to_statement_class_dict = {
            "debit": VenmoStatement.VenmoStatement
        }
        super().__init__(type_to_statement_class_dict=type_to_statement_class_dict, **kwargs)

    def update_accounts(self):
        parser = VenmoParser.VenmoParser(parent_bank=self, cookies_path=None)
        parser.update_statements()
