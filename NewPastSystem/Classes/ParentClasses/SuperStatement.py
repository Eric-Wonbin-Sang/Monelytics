import pandas

from NewPastSystem.Classes.ParentClasses import Statement

from General import Functions

pandas.set_option('display.max_columns', None)
pandas.set_option('display.expand_frame_repr', False)
pandas.set_option('display.max_colwidth', 100)


class SuperStatement:

    def __init__(self, statement_list):

        self.statement_list = statement_list

        self.super_statement_df = self.get_super_statement_df()

    def get_super_statement_df(self):
        super_statement_df = pandas.DataFrame(data={col_name: [] for col_name in Statement.Statement.col_name_list})
        for statement in self.statement_list:
            super_statement_df = super_statement_df.append(statement.statement_df)
        super_statement_df = super_statement_df.sort_index()
        return super_statement_df

    def update_running_total(self, starting_balance):
        running_balance_list = []
        for i, amount in enumerate(self.super_statement_df["amount"]):
            if i == 0:
                running_balance_list.append(starting_balance)
            else:
                running_balance_list.append(round(running_balance_list[-1] + amount, 2))
        self.super_statement_df["running_balance"] = running_balance_list

    def __str__(self):
        statement_df = self.super_statement_df.copy()

        if statement_df.empty:
            return "empty dataframe"

        statement_df = statement_df.applymap(lambda x: Functions.str_to_length(x, 20, do_dots=True, do_left=True))
        statement_df.columns = statement_df.columns.map(lambda x: Functions.str_to_length(x, 20, do_dots=True, do_left=True))
        statement_df.index = statement_df.index.map(lambda x: Functions.str_to_length(x, 14, do_dots=True, do_left=True))
        return statement_df.to_string()
