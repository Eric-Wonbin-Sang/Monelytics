import pandas
import datetime

from Banks.Generic import Statement
from Banks.BankOfAmerica import BankOfAmericaTransaction


class BankOfAmericaStatement(Statement.Statement):

    def __init__(self, parent_account, file_name, source_directory):

        super().__init__(
            parent_account=parent_account,
            file_name=file_name,
            source_directory=source_directory
        )

        if self.data_list_list:
            self.info_dict = self.get_info_dict()
            self.dataframe = self.get_dataframe()
            
            self.start_time, self.starting_balance = self.get_start_time_and_balance()
            self.end_time, self.ending_balance = self.get_end_time_and_balance()

            self.transaction_list = self.get_transaction_list()
        else:
            # fix this by adding a 'is_current_statement' bool and running logic based on that
            self.start_time, self.end_time = None, None

        self.sort_transaction_list()
        self.update_transaction_account_balances()

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

    def get_info_dict(self):
        return {data_list[0]: float(data_list[2]) for data_list in self.data_list_list[1:5]}

    def get_dataframe(self):
        return pandas.DataFrame(self.data_list_list[8:], columns=self.data_list_list[6])

    def get_transaction_list(self):
        return [
            BankOfAmericaTransaction.BankOfAmericaTransaction(
                self,
                {self.dataframe.columns[i]: data for i, data in enumerate(list(value))}
            ) for value in self.dataframe.values
        ]
