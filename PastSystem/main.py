import matplotlib.pyplot as plt
import matplotlib.dates
import pandas as pd
import numpy as np
import datetime
import seaborn as sns

from PastSystem.Classes import SnappingCursor

from PastSystem.Banks.BankOfAmerica import BankOfAmerica
from PastSystem.Banks.Venmo import Venmo
from PastSystem.Banks.BankOfAmerica.BankOfAmericaUpdateBot import BankOfAmericaUpdateBot
from PastSystem.Banks.Venmo.VenmoUpdateBot import VenmoUpdateBot

from General import Constants, Functions


def get_account_dataframe(account_list):
    dataframe_list = []
    label_list = []
    for i, account in enumerate(account_list):
        label_list.append(
            "{}'s {}: {} balance".format(
                account.parent_bank.profile_dict["owner"],
                account.parent_bank.bank_type,
                account.info_dict["name"]
            )
        )
        data = {
            "date": [x.datetime for x in account.full_transaction_list],
            label_list[-1]: [x.account_balance for x in account.full_transaction_list]
        }
        dataframe_list.append(pd.DataFrame(data, columns=list(data.keys())))

    full_dataframe = pd.concat(dataframe_list)
    full_dataframe = full_dataframe.set_index('date')
    full_dataframe = full_dataframe.sort_index()

    copy_dataframe = full_dataframe.fillna(method='ffill')
    copy_dataframe = copy_dataframe.where(pd.notnull(copy_dataframe), 0)
    full_dataframe["sum"] = copy_dataframe.sum(axis=1)
    # full_dataframe["example"] = [i * 10 for i, x in enumerate(full_dataframe.index)]

    pd.set_option('display.expand_frame_repr', False)
    print(full_dataframe)

    return full_dataframe


def graph_account_transactions(account_list):

    full_dataframe = get_account_dataframe(account_list)

    fig, ax = plt.subplots()
    line_list = []

    date_list_list = []
    value_list_list = []
    for i, col_name in enumerate(full_dataframe):
        temp = full_dataframe.loc[full_dataframe[col_name].notnull()]
        date_list_list.append(temp.index)
        value_list_list.append(temp[col_name].tolist())

        line = ax.plot(
            date_list_list[-1],
            value_list_list[-1],
            label=col_name,
            color=sns.color_palette("Set1")[i],
            alpha=0.8,
            marker="."
        )
        line_list.append(line[0])

    snap_cursor = SnappingCursor.SnappingCursor(ax, line_list, full_dataframe)
    fig.canvas.mpl_connect('motion_notify_event', snap_cursor.on_mouse_move)

    plt.legend(loc='upper left')
    plt.grid()

    plt.show()


def graph_stack_plot(account_list):
    full_dataframe = get_account_dataframe(account_list)

    copy_dataframe = full_dataframe.fillna(method='ffill')
    copy_dataframe = copy_dataframe.where(pd.notnull(copy_dataframe), 0)

    label_list = [col_name for col_name in copy_dataframe if col_name != "sum"]
    plt.stackplot(
        copy_dataframe.index.tolist(),
        [copy_dataframe[label].tolist() for label in label_list],
        labels=label_list,
        colors=sns.color_palette("Set1"),
        alpha=0.4
    )

    plt.legend(loc='upper left')
    plt.grid()
    plt.show()


def main():

    do_update = not True

    bank_list = []
    for path in Functions.get_path_list_in_dir(Constants.bank_source_info_dir):
        if "Bank Of America" == path.split("/")[-1].split(" - ")[0]:
            if do_update:
                BankOfAmericaUpdateBot(path)
            bank_list.append(BankOfAmerica.BankOfAmerica(bank_folder_dir=path))
        if "Venmo" == path.split("/")[-1].split(" - ")[0]:
            if do_update:
                VenmoUpdateBot(path)
            bank_list.append(Venmo.Venmo(bank_folder_dir=path))

    account_list = []
    for bank in bank_list:
        if bank.profile_dict["owner"] == "Eric Sang":
            account_list += bank.abstract_account_list

    for account in account_list:
        if account.parent_bank.bank_type == "Venmo":
            # print(account)
            for t in account.full_transaction_list:
                if ("util" in t.description.lower() or "internet" in t.description.lower()) and "alex" in t.description.lower():
                    print(t.amount, t.description)

    # graph_account_transactions(account_list)
    # graph_stack_plot(account_list)


if __name__ == '__main__':
    main()
