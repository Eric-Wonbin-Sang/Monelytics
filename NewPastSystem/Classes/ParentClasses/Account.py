import os
import plotly.graph_objects as go
import plotly
import flask

from General import Functions, Constants


class Account:

    def __init__(self, parent_bank, dir_name, is_temp=False, **kwargs):

        self.parent_bank = parent_bank
        self.dir_name = dir_name if dir_name else self.get_dir_name()
        self.dir_path = self.parent_bank.accounts_dir_path + "/" + self.dir_name
        self.statement_source_files_path = self.dir_path + "/source_files"
        self.account_json_path = self.dir_path + "/" + "account.json"
        self.super_statement_path = self.dir_path + "/" + "super_statement.p"
        self.super_statement_pd = self.get_super_statement_pd()

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

        if dir_name is None and not is_temp:
            self.initialize_account_structure()

        self.graph_url = self.get_graph_div()

    def get_dir_name(self):
        count = 1
        num_list = []
        for account_dir in os.listdir(self.parent_bank.accounts_dir_path):
            num_list.append(int(account_dir.split("_")[-1]))
        while True:
            if count not in num_list:
                return "account_{}".format(str(count).rjust(2, "0"))
            count += 1

    def get_super_statement_pd(self):
        if os.path.exists(self.super_statement_path):
            return Functions.unpickle(self.super_statement_path)
        return None

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

    def initialize_account_structure(self):
        os.mkdir(self.parent_bank.accounts_dir_path + "/" + self.dir_name)
        os.mkdir(self.statement_source_files_path)
        print(self.account_dict)
        print("----------")
        Functions.dict_to_json(self.account_dict, self.account_json_path)

    def to_dict(self):
        return {
            "name": self.name,
            "nickname": self.nickname,
            "type": self.type,
            "specific_type": self.specific_type,
            "curr_balance": self.curr_balance,
        }

    def get_graph_div(self):

        if self.super_statement_pd is None:
            return None

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=self.super_statement_pd.index,
                                 y=self.super_statement_pd["running_balance"],
                                 mode='lines+markers',
                                 name='lines+markers'))
        # print("\ttraces created")
        div = plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')

        # fig.show()  # this is just to see it in browser in case you want to, it isn't necessary.
        # html = fig.to_html(full_html=True, include_plotlyjs=True)
        # print(html)
        # print("\tdiv created:", div)

        return flask.Markup(div)

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


def graph_accounts(account_list):

    fig = go.Figure()
    for account in account_list:
        if account.super_statement_pd is None:
            continue

        fig.add_trace(go.Scatter(
            x=account.super_statement_pd.index,
            y=[float(data) for data in account.super_statement_pd["running_balance"]],
            mode='lines+markers',
            name=account.name)
        )

    fig.update_layout(
        # template='simple_white',
        yaxis_title='Time',
        title='Accounts',
        hovermode="x"
    )

    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ))

    graph_filepath = Constants.temp_download_dir + "/accounts_graph.html"
    fig.write_html(graph_filepath)
    return graph_filepath
