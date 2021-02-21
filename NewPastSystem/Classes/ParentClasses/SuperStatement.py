import os
import pandas

from NewPastSystem.Classes.ParentClasses import Statement

from General import Functions

pandas.set_option('display.max_columns', None)
pandas.set_option('display.expand_frame_repr', False)
pandas.set_option('display.max_colwidth', 100)


class SuperStatement:

    def __init__(self, statement_list, super_statement_path):

        self.statement_list = statement_list
        self.super_statement_path = super_statement_path

        self.super_statement_df = self.get_super_statement_df()
        self.save()

    def get_super_statement_df(self):
        super_statement_df = pandas.DataFrame(data={col_name: [] for col_name in Statement.Statement.col_name_list[1:]})
        for statement in self.statement_list:
            super_statement_df = super_statement_df.append(statement.statement_df)
        super_statement_df = super_statement_df.sort_index(ascending=False)
        return super_statement_df

    def update_running_total(self, starting_balance):
        # THIS SHOULD BE IN BOFA CREDIT CREDIT STATEMENT
        running_balance_list = []
        for i, amount in enumerate(self.super_statement_df["amount"]):
            if i == 0:
                running_balance_list.append(starting_balance)
            else:
                running_balance_list.append(round(running_balance_list[-1] + amount, 2))
        self.super_statement_df["running_balance"] = running_balance_list

    def save(self):
        if os.path.exists(self.super_statement_path):
            os.remove(self.super_statement_path)
        Functions.pickle_this(self.super_statement_df, self.super_statement_path)

    def __str__(self):
        return Functions.df_to_str(self.super_statement_df)
