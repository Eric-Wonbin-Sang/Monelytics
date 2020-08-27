import pandas

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
            self.transaction_list = self.get_transaction_list()

        # print(self.info_dict)

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
