import datetime
import operator

from General import Functions


class Statement:

    def __init__(self, parent_account, file_name, source_directory):

        self.curr_time = datetime.datetime.now()

        self.parent_account = parent_account

        self.start_time = None
        self.end_time = None
        self.starting_balance = None
        self.ending_balance = None

        self.file_name = file_name
        self.source_directory = source_directory
        self.file_path = self.source_directory + "/" + self.file_name

        self.data_list_list = Functions.csv_to_list_list(self.file_path)

        self.info_dict = {}

        self.dataframe = None
        self.transaction_list = []

    def get_transaction_list(self):
        print(type(self), "does not have an overwritten get_transaction_list function!")
        return []

    def get_times_as_current_statement(self):
        base_date_str = self.curr_time.strftime("%m-{}-%Y")
        start_date_str = base_date_str.format("01")
        end_date_str = base_date_str.format(self.curr_time.strftime("%d"))
        return \
            datetime.datetime.strptime(start_date_str, "%m-%d-%Y"), datetime.datetime.strptime(end_date_str, "%m-%d-%Y")

    def sort_transaction_list(self):
        return sorted(self.transaction_list, key=operator.attrgetter("datetime"), reverse=True)

    def update_transaction_account_balances(self):
        amount = self.starting_balance
        for transaction in self.transaction_list:
            amount += transaction.amount
            transaction.account_balance = amount
