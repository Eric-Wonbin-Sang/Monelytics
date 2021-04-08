import os
import pandas

from General import Functions


class StatementManager:

    """
    This class should be used by Accounts for converting downloaded statements to clean statement CSVs.
    """

    def __init__(self, parent_account, type_to_statement_class_dict):

        self.parent_account = parent_account
        self.type_to_statement_class_dict = type_to_statement_class_dict

        self.statement_list = self.get_statement_list()

        self.remove_clean_statement_CSVs()
        self.create_clean_statement_CSVs()

        self.super_statement_df = self.get_super_statement_df()
        self.update_super_statement_csv()

    def get_statement_list(self):
        statement_list = []
        for path in os.listdir(self.parent_account.statement_source_files_dir):
            file_path = self.parent_account.statement_source_files_dir + "/" + path
            if self.parent_account.type in self.type_to_statement_class_dict:
                statement_list.append(
                    self.type_to_statement_class_dict[self.parent_account.type](
                        parent_account=self.parent_account,
                        file_path=file_path
                    )
                )
            else:
                print("UNKNOWN ACCOUNT TYPE {}".format(self.parent_account.type))

        # filtering and sorting
        statement_list = [statement for statement in statement_list if statement.clean_statement_file_path]
        statement_list.sort(key=lambda statement: statement.last_transaction_date)

        return statement_list

    def remove_clean_statement_CSVs(self):
        for statement in self.statement_list:
            if statement.clean_statement_file_name and not os.path.exists(statement.clean_statement_file_path):
                os.remove(statement.clean_statement_file_path)

    def create_clean_statement_CSVs(self):
        for statement in self.statement_list:
            if statement.clean_statement_file_name and not os.path.exists(statement.clean_statement_file_path):
                statement.statement_df.to_csv(statement.clean_statement_file_path, index=True, header=True)

    def get_super_statement_df(self):
        super_statement_df = pandas.concat(
            [
                pandas.read_csv(path)
                for path in Functions.get_path_list_in_dir(self.parent_account.clean_statement_files_dir)
            ]
        )
        super_statement_df.index = super_statement_df["date"]
        super_statement_df = super_statement_df.drop(["date"], axis=1)

        if self.parent_account.type == "credit":
            super_statement_df = update_running_total(super_statement_df, 0)

        return super_statement_df

    def update_super_statement_csv(self):
        if os.path.exists(self.parent_account.super_statement_csv_path):
            os.remove(self.parent_account.super_statement_csv_path)
        self.super_statement_df.to_csv(self.parent_account.super_statement_csv_path, index=True, header=True)

    def remove_latest_statement_files(self):
        latest_statement = self.statement_list[-1]
        # if latest_statement:
        #     latest_statement.source_statement_file_path
        #     latest_statement.clean_statement_file_path


def update_running_total(super_statement_df, starting_balance):
    running_balance_list = []
    for i, amount in enumerate(super_statement_df["amount"]):
        if i == 0:
            running_balance_list.append(starting_balance)
        else:
            running_balance_list.append(round(running_balance_list[-1] + amount, 2))
    super_statement_df["running_balance"] = running_balance_list
    return super_statement_df
