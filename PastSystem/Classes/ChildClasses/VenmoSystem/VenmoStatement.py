import pandas
import datetime

from PastSystem.Classes.ParentClasses import Statement

from General import Functions


class VenmoStatement(Statement.Statement):

    def __init__(self, parent_account, file_path):

        self.parent_account = parent_account
        self.file_path = file_path
        self.data_list_list = Functions.csv_to_list_list(self.file_path)

        self.dataframe = self.get_dataframe()

        super().__init__(
            self.parent_account,
            self.file_path,
            self.get_statement_df()
        )

    def get_dataframe(self):
        if self.data_list_list:

            temp_list_list = self.data_list_list[3:]
            for row in temp_list_list:
                del row[0]

            return pandas.DataFrame(temp_list_list, columns=self.data_list_list[2][1:])
        return None

    def get_statement_df(self):
        statement_df = pandas.DataFrame(data={col_name: [] for col_name in Statement.Statement.col_name_list})

        starting_balance = Functions.clean_money_str(self.dataframe["Beginning Balance"].iloc[0])
        ending_balance = Functions.clean_money_str(self.dataframe["Ending Balance"].iloc[-1])
        temp_dataframe = self.dataframe.drop(
            columns=[
                "Statement Period Venmo Fees",
                "Year to Date Venmo Fees",
                "Beginning Balance",
                "Ending Balance",
                "Disclaimer"
            ]
        )
        temp_dataframe = temp_dataframe.drop(temp_dataframe.index[0])
        temp_dataframe = temp_dataframe.drop(temp_dataframe.index[-1])

        statement_df["date"] = [datetime.datetime.strptime(x, "%Y-%m-%dT%H:%M:%S") for x in temp_dataframe["Datetime"]]
        statement_df["amount"] = [Functions.clean_money_str(x) for x in temp_dataframe["Amount (total)"]]
        # statement_df["running_balance"] = temp_dataframe["Running Bal."]
        statement_df["transaction_code"] = list(temp_dataframe["ID"])
        # statement_df["address"] = temp_dataframe["Description"]
        statement_df["description"] = list(temp_dataframe["Note"])
        statement_df["status"] = list(temp_dataframe["Status"])
        statement_df["funding_source"] = list(temp_dataframe["Funding Source"])
        statement_df["destination"] = list(temp_dataframe["Destination"])
        statement_df["from"] = list(temp_dataframe["From"])
        statement_df["to"] = list(temp_dataframe["To"])

        statement_df = statement_df.set_index(['date'])

        running_balance_list = []
        for i, amount in enumerate(statement_df["amount"]):

            if i == 0:
                running_balance_list.append(starting_balance + amount)
            else:
                if statement_df["funding_source"][i] in ["Venmo balance", ""]:
                    running_balance_list.append(running_balance_list[-1] + amount)
                else:
                    running_balance_list.append(running_balance_list[-1])
            running_balance_list[-1] = round(running_balance_list[-1], 2)

        statement_df["running_balance"] = running_balance_list

        return statement_df
