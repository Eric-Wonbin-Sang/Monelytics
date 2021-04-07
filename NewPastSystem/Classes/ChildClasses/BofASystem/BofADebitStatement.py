import pandas
import datetime

from NewPastSystem.Classes.ParentClasses import Statement

from General import Functions


class BofADebitStatement(Statement.Statement):

    def __init__(self, file_path):

        self.file_path = file_path
        self.data_list_list = Functions.csv_to_list_list(self.file_path)

        self.dataframe = self.get_dataframe()

        super().__init__(self.get_statement_df(), self.get_start_date(), self.get_end_date())

    def get_start_date(self):
        if self.data_list_list:
            return datetime.datetime.strptime(self.data_list_list[1][0].split(" ")[-1], "%m/%d/%Y")
        return None

    def get_end_date(self):
        if self.data_list_list:
            return datetime.datetime.strptime(self.data_list_list[4][0].split(" ")[-1], "%m/%d/%Y")
        return None

    def get_dataframe(self):
        if self.data_list_list:
            return pandas.DataFrame(self.data_list_list[8:], columns=self.data_list_list[6])
        return None

    def get_statement_df(self):
        statement_df = pandas.DataFrame(data={col_name: [] for col_name in Statement.Statement.col_name_list})
        if self.dataframe is not None:
            statement_df["date"] = [datetime.datetime.strptime(x, "%m/%d/%Y") for x in self.dataframe["Date"]]
            statement_df["amount"] = self.dataframe["Amount"]
            statement_df["running_balance"] = self.dataframe["Running Bal."]
            statement_df["description"] = self.dataframe["Description"]
        statement_df = statement_df.set_index(['date'])
        return statement_df
