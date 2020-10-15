import pandas
import datetime

from PastSystem.Banks.AbstractSystem import Transaction, AbstractStatement


class BankOfAmericaStatement(AbstractStatement.AbstractStatement):

    def __init__(self, parent_account, statement_file_path):

        super().__init__(
            parent_account=parent_account,
            statement_file_path=statement_file_path
        )

        self.start_time, self.end_time = None, None
        self.transaction_list = []

        if self.data_list_list:
            self.info_dict = self.get_info_dict()
            self.dataframe = self.get_dataframe()
            self.transaction_list = self.get_transaction_list()

            self.start_time, self.starting_balance = self.get_start_time_and_balance()
            self.end_time, self.ending_balance = self.get_end_time_and_balance()

            self.transaction_list = self.get_transaction_list()

            self.sort_transaction_list()
            self.update_transaction_account_balances()

    def get_info_dict(self):
        return {data_list[0]: float(data_list[2]) for data_list in self.data_list_list[1:5]}

    def get_start_time_and_balance(self):
        for key, value in self.info_dict.items():
            if "Beginning balance" in key:
                return datetime.datetime.strptime(key.split(" as of ")[-1], "%m/%d/%Y"), value
        return None, None

    def get_end_time_and_balance(self):
        for key, value in self.info_dict.items():
            if "Ending balance" in key:
                return datetime.datetime.strptime(key.split(" as of ")[-1], "%m/%d/%Y"), value
        return None, None

    def get_dataframe(self):
        return pandas.DataFrame(self.data_list_list[8:], columns=self.data_list_list[6])

    def get_transaction_list(self):
        transaction_list = []
        for value in self.dataframe.values:
            raw_data_dict = {self.dataframe.columns[i]: data for i, data in enumerate(list(value))}
            transaction_list.append(
                Transaction.Transaction(
                    parent_statement=self,
                    datetime=datetime.datetime.strptime(raw_data_dict["Date"], "%m/%d/%Y"),
                    amount=float(raw_data_dict["Amount"]),
                    description=raw_data_dict["Description"]
                )
            )
        return transaction_list

    def update_transaction_account_balances(self):
        amount = self.starting_balance
        for transaction in self.transaction_list:
            amount += transaction.amount
            transaction.account_balance = amount

    def __str__(self):
        return "Bank Of America Statement: "
