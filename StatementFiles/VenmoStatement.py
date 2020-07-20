import datetime as dt

from AccountParsers import Transaction
from StatementFiles import Statement

from General import Functions


class VenmoStatement(Statement.Statement):

    index_dict = {
        "datetime": 2,              # USED
        "type": 3,                  #
        "status": 4,                #
        "note": 5,                  # USED
        "from": 6,                  #
        "to": 7,                    #
        "amount": 8,                # USED
        "funding_source": 10,       # USED
        "destination": 11,          # USED
        "beginning_balance": 12,    # USED
        "ending_balance": 13        # USED
    }

    def __init__(self, **kwargs):

        self.account = kwargs.get("account")
        self.statement_path = kwargs.get("statement_path")
        self.source_list_list = Functions.csv_to_list_list(self.statement_path)
        
        self.beginning_balance = self.get_beginning_balance()
        self.ending_balance = self.get_ending_balance()

        super().__init__(
            account=kwargs.get("account"),
            transaction_list=self.get_transaction_list()
        )
        
    def get_beginning_balance(self):
        return round(float(Functions.get_first_in_list(
            Functions.get_col(self.source_list_list[1:], self.index_dict["beginning_balance"])).replace("$", "")), 2)

    def get_ending_balance(self):
        return round(float(Functions.get_first_in_list(
            Functions.get_col(self.source_list_list[1:], self.index_dict["ending_balance"])).replace("$", "")), 2)

    def get_transaction_list(self):

        transaction_list = []
        balance = self.beginning_balance
        for data_list in self.source_list_list[2:-4]:

            funding_source = data_list[self.index_dict["funding_source"]]
            destination = data_list[self.index_dict["destination"]]

            if funding_source == "Venmo balance" or destination:
                amount = round(float(data_list[self.index_dict["amount"]].replace("$", "").replace(" ", "")), 2)
            else:
                amount = 0

            balance += amount
            balance = round(balance, 2)

            # https://www.journaldev.com/23365/python-string-to-datetime-strptime
            datetime = dt.datetime.strptime(data_list[self.index_dict["datetime"]], '%Y-%m-%dT%H:%M:%S')

            transaction_list.append(
                Transaction.Transaction(
                    amount=amount,
                    description=data_list[self.index_dict["note"]],
                    datetime=datetime,
                    balance=balance,
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
