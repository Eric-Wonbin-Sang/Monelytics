from NewPastSystem.Classes.ParentClasses import Bank
from NewPastSystem.Classes.ChildClasses.DiscoverSystem import DiscoverParser, DiscoverStatement


class DiscoverBank(Bank.Bank):

    def __init__(self, profile, **kwargs):

        type_to_statement_class_dict = {
            "credit": DiscoverStatement.DiscoverStatement,
        }
        super().__init__(profile, type_to_statement_class_dict=type_to_statement_class_dict, **kwargs)

    def update_accounts(self):
        parser = DiscoverParser.DiscoverParser(parent_bank=self, cookies_path=None)
        parser.update_statements()
