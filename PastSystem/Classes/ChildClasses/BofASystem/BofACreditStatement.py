import pandas
import datetime

from PastSystem.Classes.ParentClasses import Statement

from General import Functions


class BofACreditStatement(Statement.Statement):

    default_statement_name = "transaction_period.csv"

    def __init__(self, parent_account, file_path):

        self.parent_account = parent_account
        self.file_path = file_path
        self.data_list_list = Functions.csv_to_list_list(self.file_path)

        self.dataframe = self.get_dataframe()

        super().__init__(
            parent_account,
            file_path,
            self.get_statement_df()
        )

    def get_dataframe(self):
        if self.data_list_list[1:]:
            return pandas.DataFrame(self.data_list_list[1:], columns=self.data_list_list[0])
        return None

    def get_statement_df(self):
        statement_df = pandas.DataFrame(data={col_name: [] for col_name in Statement.Statement.col_name_list})

        if self.dataframe is not None:
            statement_df["date"] = [datetime.datetime.strptime(x, "%m/%d/%Y") for x in self.dataframe["Posted Date"]]
            statement_df["amount"] = self.dataframe["Amount"]
            # statement_df["amount"] = (float(x) for x in self.dataframe["Amount"])
            # statement_df["running_balance"] = self.dataframe[""]
            statement_df["transaction_code"] = self.dataframe["Reference Number"]
            statement_df["address"] = self.dataframe["Address"]
            statement_df["description"] = self.dataframe["Payee"]
        statement_df = statement_df.set_index(['date'])
        statement_df = statement_df.iloc[::-1]

        return statement_df
