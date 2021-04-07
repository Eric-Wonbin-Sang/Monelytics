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

    def __init__(self, statement_df, start_date=None, end_date=None):

        self.statement_df = statement_df
        self.statement_df["amount"] = [float(x) for x in self.statement_df["amount"]]

        self.start_date = start_date
        self.end_date = end_date

        # print("start: {}\t\tend: {}".format(self.start_date, self.end_date))

    def __str__(self):
        statement_df = self.statement_df.copy()

        if statement_df.empty:
            return "empty dataframe"

        statement_df = statement_df.applymap(lambda x: Functions.str_to_length(x, 20, do_dots=True, do_left=True))
        statement_df.columns = statement_df.columns.map(lambda x: Functions.str_to_length(x, 20, do_dots=True, do_left=True))
        statement_df.index = statement_df.index.map(lambda x: Functions.str_to_length(x, 10, do_dots=True, do_left=True))
        return statement_df.to_string()
