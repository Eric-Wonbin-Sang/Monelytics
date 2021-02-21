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
        "description"
    ]

    def __init__(self, statement_df):

        self.statement_df = statement_df
        self.statement_df["amount"] = [float(x) for x in self.statement_df["amount"]]

    def __str__(self):
        statement_df = self.statement_df.copy()

        if statement_df.empty:
            return "empty dataframe"

        statement_df = statement_df.applymap(lambda x: Functions.str_to_length(x, 20, do_dots=True, do_left=True))
        statement_df.columns = statement_df.columns.map(lambda x: Functions.str_to_length(x, 20, do_dots=True, do_left=True))
        statement_df.index = statement_df.index.map(lambda x: Functions.str_to_length(x, 10, do_dots=True, do_left=True))
        return statement_df.to_string()
