import pandas
import datetime

from Banks.Generic import Statement
from Banks.Venmo import VenmoTransaction

from General import Functions, Constants


class VenmoStatement(Statement.Statement):

    column_pair_list = [
        ("Username", True),
        ("ID", False),
        ("Datetime", False),
        ("Type", False),
        ("Status", False),
        ("Note", False),
        ("From", False),
        ("To", False),
        ("Amount (total)", False),
        ("Amount (fee)", False),
        ("Funding Source", False),
        ("Destination", False),
        ("Beginning Balance", True),
        ("Ending Balance", True),
        ("Statement Period Venmo Fees", True),
        ("Terminal Location", False),
        ("Year to Date Venmo Fees", True),
        ("Disclaimer", True)
    ]

    def __init__(self, parent_account, file_name, source_directory):

        super().__init__(
            parent_account=parent_account,
            file_name=file_name,
            source_directory=source_directory
        )

        self.dataframe = self.get_dataframe()
        self.info_dict = self.get_info_dict()
        self.clean_dataframe()

        self.start_time, self.end_time = self.get_start_and_end_times()
        self.starting_balance = float(self.info_dict["Beginning Balance"][1:])
        self.ending_balance = float(self.info_dict["Ending Balance"][1:])

        self.transaction_list = self.get_transaction_list()

        self.sort_transaction_list()
        self.update_transaction_account_balances()

    def get_start_and_end_times(self):
        if self.file_name == Constants.current_statement_file_name_default:
            return self.get_times_as_current_statement()
        return [datetime.datetime.strptime(x, "%m-%d-%Y") for x in self.file_name[:-4].split(" to ")]

    def get_dataframe(self):
        column_headers = self.data_list_list[0]
        temp_list_list = [x for x in self.data_list_list[1:]]
        return pandas.DataFrame(temp_list_list, columns=column_headers)

    def get_info_dict(self):
        """
        Creates an info_dict where single values are saved to a dict by the columns that have a pair of True in
        column_pair_list.
        """
        info_dict = {}
        for (column_name, is_single_value) in self.column_pair_list:
            if is_single_value:
                value = None
                for data in self.dataframe[column_name].values:
                    if data != "":
                        value = data
                info_dict[column_name] = value
        return info_dict

    def clean_dataframe(self):
        """
        Deletes columns in dataframe that are single values specified by column_pair_list. Deletes empty rows. Also
        erases the empty - and -1 index rows.
        """
        for (column_name, is_single_value) in self.column_pair_list:
            if is_single_value:
                self.dataframe.drop(column_name, axis=1, inplace=True)
        self.dataframe.drop(0, axis=0, inplace=True)
        self.dataframe.drop(self.dataframe.tail(1).index, axis=0, inplace=True)

    def get_transaction_list(self):
        return [
            VenmoTransaction.VenmoTransaction(
                self,
                {self.dataframe.columns[i]: data for i, data in enumerate(list(value))}
            ) for value in self.dataframe.values
        ]

    def update_transaction_account_balances(self):
        amount = self.starting_balance
        for transaction in self.transaction_list:
            if not (transaction.raw_data_dict["Funding Source"] != "Venmo balance" and transaction.amount < 0):
                amount += transaction.amount
            transaction.account_balance = amount
