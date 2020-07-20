import datetime as dt

from AccountParsers import Transaction
from StatementFiles import Statement

from General import Functions


class BofAStatement(Statement.Statement):
    
    index_dict = {
        "date": 0,
        "description": 1,
        "amount": 2,
        "balance": 3
    }

    def __init__(self, **kwargs):

        self.account = kwargs.get("account")
        self.statement_path = kwargs.get("statement_path")
        self.source_list_list = Functions.csv_to_list_list(self.statement_path)

        super().__init__(transaction_list=self.get_transaction_list())

    def get_header_and_data_list_list(self):
        for i, row in enumerate(self.source_list_list):
            if not row:
                return self.source_list_list[:i], self.source_list_list[i + 1:]
        return [], []

    def get_transaction_list(self):

        header_list_list, data_list_list = self.get_header_and_data_list_list()

        transaction_list = []
        for data_list in data_list_list[1:]:

            datetime = dt.datetime.strptime(data_list[self.index_dict["date"]], '%m/%d/%Y')

            transaction_list.append(
                Transaction.Transaction(
                    amount=data_list[self.index_dict["amount"]],
                    description=data_list[self.index_dict["description"]],
                    datetime=datetime,
                    balance=data_list[self.index_dict["balance"]],
                    account=self.account
                )
            )

        return transaction_list

    def __str__(self):
        ret_str = ""
        i = 1
        if i == 0:
            for d_i, day in enumerate(self.day_transaction_list_dict):
                if d_i != 0:
                    ret_str += "\n"
                ret_str += "Day: {}".format(day)
                for transaction in self.day_transaction_list_dict[day]:
                    ret_str += "\n\t{}".format(transaction)
            return ret_str
        else:
            for d_i, day in enumerate(self.day_transaction_list_dict):
                if d_i != 0:
                    ret_str += "\n"
                ret_str += "{} Day: {} - transaction count: {}".format(d_i, day, len(self.day_transaction_list_dict[day]))
            return ret_str
