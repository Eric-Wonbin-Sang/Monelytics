import pandas
import datetime

from Banks.AbstractSystem import AbstractStatement, Transaction


class VenmoStatement(AbstractStatement.AbstractStatement):

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

    def __init__(self, parent_account, statement_file_path):

        super().__init__(
            parent_account=parent_account,
            statement_file_path=statement_file_path
        )

        self.dataframe = self.get_dataframe()

        self.info_dict = self.get_info_dict()
        self.clean_dataframe()

        self.start_time, self.end_time = self.get_start_and_end_times()
        self.starting_balance = self.get_starting_balance()
        self.ending_balance = self.get_ending_balance()

        self.transaction_list = self.get_transaction_list()

        self.sort_transaction_list()

    def get_times_as_current_statement(self):
        base_date_str = self.curr_time.strftime("%m-{}-%Y")
        start_date_str = base_date_str.format("01")
        end_date_str = base_date_str.format(self.curr_time.strftime("%d"))
        return \
            datetime.datetime.strptime(start_date_str, "%m-%d-%Y"), datetime.datetime.strptime(end_date_str, "%m-%d-%Y")

    def get_start_and_end_times(self):
        if self.is_current_statement:
            return self.get_times_as_current_statement()
        return [datetime.datetime.strptime(x, "%m-%d-%Y")
                for x in self.statement_file_path.split("/")[-1][:-4].split(" to ")]

    def get_starting_balance(self):
        return float(self.info_dict["Beginning Balance"][1:].replace(",", ""))

    def get_ending_balance(self):
        return float(self.info_dict["Ending Balance"][1:].replace(",", ""))

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

        def get_amount():
            is_positive = raw_data_dict["Amount (total)"][0] == "+"
            number = float(raw_data_dict["Amount (total)"][3:].replace(",", ""))
            return number if is_positive else number * -1

        def get_description():
            if raw_data_dict["From"] == "" and raw_data_dict["To"] == "":
                return "Moved funds to {}".format(raw_data_dict["Destination"])
            return "From {} to {}: ".format(raw_data_dict["From"], raw_data_dict["To"]) + raw_data_dict["Note"]

        amount = self.starting_balance
        transaction_list = []
        for value in self.dataframe.values:
            raw_data_dict = {self.dataframe.columns[i]: data for i, data in enumerate(list(value))}
            transaction_list.append(
                Transaction.Transaction(
                    parent_statement=self,
                    datetime=datetime.datetime.strptime(raw_data_dict["Datetime"], "%Y-%m-%dT%H:%M:%S"),
                    amount=get_amount(),
                    description=get_description()
                )
            )
            if not (raw_data_dict["Funding Source"] != "" and raw_data_dict["Funding Source"] != "Venmo balance"):
                amount += transaction_list[-1].amount
            transaction_list[-1].account_balance = amount

        return transaction_list
