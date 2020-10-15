import matplotlib.pyplot as plt

from PastSystem.Banks.BankOfAmerica import BankOfAmerica
from PastSystem.Banks.Venmo import Venmo
from PastSystem.Banks.BankOfAmerica.BankOfAmericaUpdateBot import BankOfAmericaUpdateBot
from PastSystem.Banks.Venmo.VenmoUpdateBot import VenmoUpdateBot

from General import Constants, Functions


def graph_account_transactions(account_list):
    color_list = "bgrcmyk"
    for i, account in enumerate(account_list):
        plt.plot(
            [x.datetime for x in account.full_transaction_list],
            [x.account_balance for x in account.full_transaction_list],
            color=color_list[i],
            label=account.parent_bank.profile_dict["owner"] + "'s " + account.parent_bank.bank_type + ": " + account.info_dict["name"] + " balance"
        )
    plt.legend()
    plt.show()


def main():

    do_update = False

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
        # print(bank_list[-1])

    account_list = []
    for bank in bank_list:
        account_list += bank.abstract_account_list
    # graph_account_transactions(account_list)

    # graph_account_transactions([account for account in account_list if account.parent_bank.bank_type == "Venmo"])

    eric_venmo_account = None
    for bank in bank_list:
        if bank.bank_type == "Venmo" and bank.profile_dict["owner"] == "Eric Sang":
            eric_venmo_account = bank.abstract_account_list[0]
            break

    for t in eric_venmo_account.full_transaction_list:
        print(t)
    graph_account_transactions([eric_venmo_account])


main()
