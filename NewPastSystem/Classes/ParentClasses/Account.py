import os
import pandas
import plotly.graph_objects as go

from NewPastSystem.Classes.ParentClasses import StatementManager, SuperStatement

from General import Functions, Constants


class Account:

    def __init__(self, parent_bank, dir_name, type_to_statement_class_dict, is_temp=False, **kwargs):

        self.parent_bank = parent_bank
        self.dir_name = dir_name if dir_name else self.get_dir_name()
        self.dir_path = self.parent_bank.accounts_dir_path + "/" + self.dir_name

        self.statement_source_files_dir = self.dir_path + "/source_files"
        self.clean_statement_files_dir = self.dir_path + "/clean_statements"

        self.account_json_path = self.dir_path + "/" + "account.json"

        self.super_statement_csv_name = "super_statement.csv"
        self.super_statement_csv_path = self.dir_path + "/" + self.super_statement_csv_name

        self.name = kwargs.get("name")
        self.nickname = kwargs.get("nickname")
        self.type = kwargs.get("type")
        self.specific_type = kwargs.get("specific_type")
        self.curr_balance = kwargs.get("curr_balance")
        self.account_number = kwargs.get("account_number")
        self.routing_number_dict = kwargs.get("routing_number_dict")
        self.opened_date = kwargs.get("opened_date")
        self.account_url = kwargs.get("account_url")
        self.account_dict = self.get_account_dict()

        if not is_temp:
            self.check_dirs()

        self.statement_cleaner = StatementManager.StatementManager(
            self,
            type_to_statement_class_dict=type_to_statement_class_dict
        )
        self.update_curr_balance()

    def get_dir_name(self):
        count = 1
        num_list = []
        for account_dir in os.listdir(self.parent_bank.accounts_dir_path):
            num_list.append(int(account_dir.split("_")[-1]))
        while True:
            if count not in num_list:
                return "account_{}".format(str(count).rjust(2, "0"))
            count += 1

    def get_account_dict(self):
        return {
            "name": self.name,
            "nickname": self.nickname,
            "type": self.type,
            "specific_type": self.specific_type,
            "curr_balance": self.curr_balance,
            "account_number": self.account_number,
            "routing_number_dict": self.routing_number_dict,
            # "opened_date": self.opened_date,
            "account_url": self.account_url
        }

    def check_dirs(self):
        if not os.path.exists(self.statement_source_files_dir):
            os.mkdir(self.statement_source_files_dir)
        if not os.path.exists(self.clean_statement_files_dir):
            os.mkdir(self.clean_statement_files_dir)
        if not os.path.exists(self.account_json_path):
            Functions.dict_to_json(self.account_dict, self.account_json_path)

    def update_curr_balance(self):
        self.curr_balance = self.statement_cleaner.super_statement_df["running_balance"][-1]

        self.account_dict = self.get_account_dict()
        if not os.path.exists(self.account_json_path):
            os.remove(self.account_json_path)
        Functions.dict_to_json(self.account_dict, self.account_json_path)

    def to_dict(self):
        return {
            "name": self.name,
            "nickname": self.nickname,
            "type": self.type,
            "specific_type": self.specific_type,
            "curr_balance": self.curr_balance,
        }

    def __str__(self):
        return "Account - child of {}_id{}\n\t{}\n\t{}\n\t{}\n\t{}\n\t{}\n\t{}\n\t{}".format(
            self.parent_bank.type,
            self.name,
            self.nickname,
            self.type,
            self.specific_type,
            self.account_number,
            self.routing_number_dict,
            self.opened_date,
            self.account_url
        )


def graph_accounts(profile, account_list):

    fig = go.Figure()
    for account in account_list:

        if account.statement_cleaner.super_statement_df is None:
            continue

        fig.add_trace(go.Scatter(
            x=account.statement_cleaner.super_statement_df.index,
            y=[float(data) for data in account.statement_cleaner.super_statement_df["running_balance"]],
            mode='lines+markers',
            name=account.name)
        )

    fig.update_layout(
        # template='simple_white',
        xaxis_title='Time',
        yaxis_title='Amount',
        title='Accounts',
        hovermode="x",
        legend={
            "yanchor": "top",
            "y": 0.99,
            "xanchor": "left",
            "x": 0.01
        }
    )

    fig.write_html(profile.past_system_graph_path)
    return profile.past_system_graph_path


def get_all_account_transaction_dict_list(account_list):

    super_statement_df_list = []
    for account in account_list:
        if account.statement_cleaner.super_statement_df is None:
            continue
        temp_super_statement_pd = account.statement_cleaner.super_statement_df
        temp_super_statement_pd["parent_bank_type"] = account.parent_bank.type
        temp_super_statement_pd["parent_bank_owner"] = account.parent_bank.owner
        temp_super_statement_pd["account_name"] = account.name
        super_statement_df_list.append(temp_super_statement_pd)
    super_super_statement_pd = pandas.concat(super_statement_df_list)
    super_super_statement_pd = super_super_statement_pd.sort_index()

    transaction_dict_list = []
    for index, row in super_super_statement_pd.iterrows():
        transaction_dict_list.append(
            {
                "date": str(index),
                "parent_bank_type": str(row["parent_bank_type"]),
                "parent_bank_owner": str(row["parent_bank_owner"]),
                "account_name": str(row["account_name"]),
                "from": str(row["from"]) if str(row["from"]) != "nan" else "--",
                "amount": str(row["amount"]),
                "description": str(row["description"]) if str(row["from"]) != "nan" else "--",
            }
        )
    return list(reversed(transaction_dict_list))[:50]
