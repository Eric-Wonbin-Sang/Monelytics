
from General import Functions


class Transaction:

    def __init__(self, **kwargs):

        self.parent_statement = kwargs["parent_statement"]

        self.datetime = kwargs["datetime"]
        self.amount = kwargs["amount"]
        self.description = kwargs["description"]

        print(self)

    def __str__(self):
        return " | ".join(
            [str(x) for x in [
                self.datetime,
                Functions.str_to_length(self.parent_statement.parent_account.parent_bank.name, 10),
                Functions.str_to_length(self.parent_statement.parent_account.name, 20),
                Functions.str_to_length(self.amount, 10, do_dots=False, do_left=False),
                self.description
            ]]
        )
