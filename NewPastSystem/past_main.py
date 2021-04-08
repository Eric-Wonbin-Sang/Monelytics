import os

from NewPastSystem.Classes.ParentClasses import Bank, Account
from NewPastSystem.Classes.ChildClasses.BofASystem import BofABank
from NewPastSystem.Classes.ChildClasses.DiscoverSystem import DiscoverBank
from NewPastSystem.Classes.ChildClasses.VenmoSystem import VenmoBank
from NewPastSystem.Classes.ChildClasses.ChaseSystem import ChaseBank

from General import Functions, Constants


type_to_bank_class_dict = {
    "Bank of America": BofABank.BofABank,
    "Discover": DiscoverBank.DiscoverBank,
    "Chase": ChaseBank.ChaseBank,
    "Venmo": VenmoBank.VenmoBank,
    # "Mint": Bank.Bank
}


def get_existing_bank_list(banks_dir):
    existing_bank_list = []
    for dir_name in os.listdir(banks_dir):

        if not os.path.isdir(banks_dir + "/" + dir_name):
            continue

        bank_json_path = banks_dir + "/" + dir_name + "/" + "bank.json"
        bank_dict = Functions.parse_json(bank_json_path)

        bank_class = type_to_bank_class_dict.get(bank_dict["type"])
        if bank_class:
            existing_bank_list.append(bank_class(dir_name=dir_name, **bank_dict))
            print("Found Bank:", existing_bank_list[-1].type, existing_bank_list[-1].username)
        else:
            print("unknown bank type:", bank_dict["type"])
    return existing_bank_list


def get_bank_list(bank_dict_list, existing_bank_list):
    bank_list = []
    for bank_dict in bank_dict_list:

        if bank_dict in [existing_bank.bank_dict for existing_bank in existing_bank_list]:
            continue

        bank_class = type_to_bank_class_dict.get(bank_dict["type"])
        if bank_class:
            bank_list.append(bank_class(dir_name=None, **bank_dict))
            print("Created Bank:", bank_list[-1].type, bank_list[-1].username)
        else:
            print("unknown bank type:", bank_dict["type"])
    return bank_list


def get_full_bank_list():
    existing_bank_list = get_existing_bank_list(Constants.banks_dir)
    bank_dict_list = Functions.parse_json(Constants.bank_logins_json)
    new_bank_list = get_bank_list(bank_dict_list, existing_bank_list)
    return existing_bank_list + new_bank_list


def main():

    bank_list = get_full_bank_list()
    # for bank in bank_list:
    #     # if bank.type in ["Chase"]:
    #     #     bank.update_accounts()
    #     #     Account.graph_accounts(bank.account_list)
    #     print(bank.type)

    # account_list = [account for bank in bank_list for account in bank.account_list]

    # Account.get_all_account_transaction_dict_list(account_list)

    # graph_account_transactions(bank_list)


if __name__ == '__main__':
    main()
