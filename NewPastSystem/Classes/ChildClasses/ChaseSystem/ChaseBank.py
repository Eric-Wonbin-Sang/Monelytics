from NewPastSystem.Classes.ParentClasses import Bank
from NewPastSystem.Classes.ChildClasses.ChaseSystem import ChaseParser, ChaseDebitStatement, ChaseCreditStatement


class ChaseBank(Bank.Bank):

    def __init__(self, profile, **kwargs):

        type_to_statement_class_dict = {
            "debit": ChaseDebitStatement.ChaseDebitStatement,
            "credit": ChaseCreditStatement.ChaseCreditStatement
        }
        super().__init__(profile, type_to_statement_class_dict=type_to_statement_class_dict, **kwargs)

    def update_accounts(self):
        parser = ChaseParser.ChaseParser(parent_bank=self, cookies_path=None)
        parser.update_statements()
