import operator
import matplotlib.pyplot as plt

from Banks.AbstractSystem import AbstractBank
from Banks.BankOfAmerica.BankOfAmericaUpdateBot import BankOfAmericaUpdateBot
from Banks.Venmo.VenmoUpdateBot import VenmoUpdateBot

from General import Constants, Functions


def sort_transaction_list(transaction_list):
    return sorted(transaction_list, key=operator.attrgetter("datetime"), reverse=False)


def account_to_transaction_list(account):
    transaction_list = []
    for statement in account.statement_list:
        transaction_list += statement.transaction_list
    return sort_transaction_list(transaction_list)


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

    # for path in Functions.get_path_list_in_dir(Constants.new_bank_source_info_dir):
    #     # if "Bank Of America" == path.split("/")[-1].split(" - ")[0]:
    #     #     BankOfAmericaUpdateBot(path)
    #     if "Venmo" == path.split("/")[-1].split(" - ")[0]:
    #         VenmoUpdateBot(path)

    bank_list = []
    for path in Functions.get_path_list_in_dir(Constants.new_bank_source_info_dir):
        bank_list.append(AbstractBank.AbstractBank(bank_folder_dir=path))
        print(bank_list[-1])


main()
