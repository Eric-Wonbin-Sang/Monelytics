import operator
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from mpl_finance import candlestick_ohlc
from matplotlib.dates import date2num

from Classes import Profile


def sort_transaction_list(transaction_list):
    return sorted(transaction_list, key=operator.attrgetter("datetime"), reverse=False)


def account_to_transaction_list(account):
    transaction_list = []
    for statement in account.statement_list:
        transaction_list += statement.transaction_list
    return sort_transaction_list(transaction_list)


def do_candlestick(transaction_list):

    datetime_transaction_list_dict = {}
    for transaction in transaction_list:
        if transaction.datetime not in datetime_transaction_list_dict:
            datetime_transaction_list_dict[transaction.datetime] = []
        datetime_transaction_list_dict[transaction.datetime] += [transaction]

    for key, value in datetime_transaction_list_dict.items():
        datetime_transaction_list_dict[key] = sort_transaction_list(value)

    data_list_list = []
    for datetime, t_list in datetime_transaction_list_dict.items():
        data_list_list.append(
            [
                date2num(datetime),                 # date
                t_list[0].account_balance,          # openp
                max([t.account_balance for t in t_list]),    # highp
                min([t.account_balance for t in t_list]),    # lowp
                t_list[-1].account_balance,         # closep
                len(t_list)                         # volume
            ]
        )

    # fig = plt.figure()
    ax1 = plt.subplot2grid((1, 1), (0, 0))

    candlestick_ohlc(ax1, data_list_list, width=0.4, colorup='#77d879', colordown='#db3f3f')

    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(45)

    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax1.grid(True)

    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()


def graph_account_transactions(account_list):
    for i, account in enumerate(account_list):
        transaction_list = account_to_transaction_list(account)
        plt.plot(
            [x.datetime for x in transaction_list],
            [x.account_balance for x in transaction_list],
            color="bgrcmykw"[i],
            label=account.parent_bank.name + ": " + account.name + " balance"
        )
    plt.legend()
    plt.show()


def main():

    profile_list = Profile.get_profile_list()

    account_list = [account for profile in profile_list for account in profile.bank.account_list]
    graph_account_transactions(account_list)

    full_transaction_list = []
    for account in account_list:
        full_transaction_list += account_to_transaction_list(account)
    full_transaction_list = sort_transaction_list(full_transaction_list)
    # do_candlestick(full_transaction_list)


main()
