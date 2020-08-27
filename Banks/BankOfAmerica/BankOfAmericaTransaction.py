import datetime

from Banks.Generic import Transaction


class BankOfAmericaTransaction(Transaction.Transaction):

    def __init__(self, parent_statement, raw_data_dict):

        self.raw_data_dict = raw_data_dict

        super().__init__(
            parent_statement=parent_statement,
            datetime=datetime.datetime.strptime(raw_data_dict["Date"], "%m/%d/%Y"),
            amount=float(raw_data_dict["Amount"]),
            description=raw_data_dict["Description"]
        )
