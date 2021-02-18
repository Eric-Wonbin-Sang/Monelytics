from General import Functions


class Transaction:

    def __init__(self, **kwargs):

        self.init_kwargs = kwargs

        self.date = kwargs.get("date")
        self.description = kwargs.get("description")
        self.original_description = kwargs.get("original_description")
        self.amount = kwargs.get("amount")

        self.transaction_type = kwargs.get("transaction_type")
        self.is_debit, self.is_credit = (True, False) if self.transaction_type == "debit" else (False, True)

        self.category = kwargs.get("category")
        self.account_name = kwargs.get("account_name")
        self.labels = kwargs.get("labels")
        self.notes = kwargs.get("notes")

    def __str__(self):
        return " | ".join(
            [
                Functions.str_to_length(self.date, 10, do_dots=False),
                Functions.str_to_length(self.account_name, 19, do_dots=False),
                # Functions.str_to_length(self.amount, 7, do_dots=True),
                str(self.amount).center(7),
                # Functions.str_to_length(self.description, 24, do_dots=True),
                # Functions.str_to_length(self.original_description, 24, do_dots=True),
                str(self.init_kwargs)
            ]
        )
