import pandas

from General import Functions

pandas.set_option('display.max_columns', None)
pandas.set_option('display.expand_frame_repr', False)
pandas.set_option('display.max_colwidth', 100)


class Statement:

    col_name_list = [
        "date",
        "amount",
        "running_balance",
        "transaction_code",
        "address",
        "description",
        "status",           # added from Venmo
        "funding_source",   # added from Venmo
        "destination",      # added from Venmo
        "from",             # added from Venmo
        "to",               # added from Venmo
    ]

    def __init__(self, parent_account, source_statement_file_path, statement_df):

        self.parent_account = parent_account
        self.source_statement_file_path = source_statement_file_path
        self.statement_df = statement_df

        self.statement_df["amount"] = [float(x) for x in self.statement_df["amount"]]
        self.is_empty = self.statement_df.empty

        self.first_transaction_date = self.statement_df.iloc[[0]].index[0] if not self.is_empty else None
        self.last_transaction_date = self.statement_df.iloc[[-1]].index[0] if not self.is_empty else None
        self.clean_statement_file_name = self.get_clean_statement_file_name()
        self.clean_statement_file_path = self.get_clean_statement_file_path()

    def get_clean_statement_file_name(self):
        if self.first_transaction_date is not None and self.last_transaction_date is not None:
            return "{} to {} Transactions.csv".format(
                self.first_transaction_date.strftime("%Y-%m-%d"),
                self.last_transaction_date.strftime("%Y-%m-%d"),
            )
        return None

    def get_clean_statement_file_path(self):
        if self.clean_statement_file_name:
            return self.parent_account.clean_statement_files_dir + "/" + self.clean_statement_file_name
        return None

    def __str__(self):
        statement_df = self.statement_df.copy()

        if statement_df.empty:
            return "empty dataframe"

        statement_df = statement_df.applymap(lambda x: Functions.str_to_length(x, 20, do_dots=True, do_left=True))
        statement_df.columns = statement_df.columns.map(lambda x: Functions.str_to_length(x, 20, do_dots=True, do_left=True))
        statement_df.index = statement_df.index.map(lambda x: Functions.str_to_length(x, 10, do_dots=True, do_left=True))
        return statement_df.to_string()
