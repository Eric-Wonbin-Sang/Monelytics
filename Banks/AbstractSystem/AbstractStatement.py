import datetime
import operator

from General import Functions, Constants


class AbstractStatement:

    def __init__(self, parent_account, statement_file_path):

        self.curr_time = datetime.datetime.now()

        self.parent_account = parent_account
        self.statement_file_path = statement_file_path
        self.is_current_statement = self.get_is_current_statement()

        self.data_list_list = self.get_data_list_list()

        self.start_time = None
        self.end_time = None
        self.starting_balance = None
        self.ending_balance = None
        self.transaction_list = []

    def get_is_current_statement(self):
        return self.statement_file_path.split("/")[-1] == Constants.current_statement_file_name_default

    def get_data_list_list(self):
        return Functions.csv_to_list_list(self.statement_file_path)

    # def get_start_and_end_times(self):
    #     pass
    #     return None, None
    #
    # def get_starting_balance(self):
    #     return None
    #
    # def get_ending_balance(self):
    #     return None
    #
    # def get_transaction_list(self):
    #     return []

    def sort_transaction_list(self):
        return sorted(self.transaction_list, key=operator.attrgetter("datetime"), reverse=True)

    def __str__(self):
        return self.statement_file_path
