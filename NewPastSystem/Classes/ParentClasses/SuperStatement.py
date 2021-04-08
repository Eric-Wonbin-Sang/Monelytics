import pandas

from General import Functions

pandas.set_option('display.max_columns', None)
pandas.set_option('display.expand_frame_repr', False)
pandas.set_option('display.max_colwidth', 100)


class SuperStatement:

    def __init__(self, parent_account, statement_list, super_statement_path):

        self.parent_account = parent_account
        self.statement_list = statement_list
        self.super_statement_path = super_statement_path

        self.super_statement_df = self.get_super_statement_df()

    def get_super_statement_df(self):
        super_dataframe = pandas.read_csv(self.parent_account.super_statement_csv_path)
        super_dataframe.index = super_dataframe["date"]
        super_dataframe = super_dataframe.drop(["date"], axis=1)
        # super_dataframe = super_dataframe.sort_index(ascending=False)
        return super_dataframe

    def __str__(self):
        return Functions.df_to_str(self.super_statement_df)
