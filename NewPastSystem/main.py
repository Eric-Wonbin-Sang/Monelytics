import os
import numpy
import pandas
import datetime
import seaborn as sns
import matplotlib.dates
import matplotlib.pyplot as plt

from NewPastSystem.Classes.ParentClasses import Bank
from NewPastSystem.Classes.ChildClasses.BofASystem import BofABank
from NewPastSystem.Classes.ChildClasses.DiscoverSystem import DiscoverBank
from NewPastSystem.Classes.ChildClasses.VenmoSystem import VenmoBank

from General import Functions, Constants


type_to_bank_class_dict = {
    "Bank of America": BofABank.BofABank,
    "Discover": DiscoverBank.DiscoverBank,
    "Chase": Bank.Bank,
    "Venmo": VenmoBank.VenmoBank,
    "Mint": Bank.Bank
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


def graph_account_transactions(bank_list):

    result_df_list = []
    for bank in bank_list:
        for account in bank.account_list:

            if account.super_statement_pd is None:
                break

            temp_df = account.super_statement_pd[["running_balance"]]
            temp_df = temp_df.rename(columns={"running_balance": account.name})

            result_df_list.append(temp_df)

    # for result_df in result_df_list:
    #     # result_df = result_df.fillna(method='ffill')
    #     # result_df = result_df.where(pandas.notnull(result_df), 0)
    #     try:
    #         print(result_df)
    #         result_df.plot()
    #         plt.legend(loc='upper left')
    #         plt.show()
    #     except:
    #         pass


def main():

    existing_bank_list = get_existing_bank_list(Constants.banks_dir)
    bank_dict_list = Functions.parse_json(Constants.bank_logins_json)
    new_bank_list = get_bank_list(bank_dict_list, existing_bank_list)

    bank_list = existing_bank_list + new_bank_list
    for bank in bank_list:
        print(bank)

    # graph_account_transactions(bank_list)


# def add_number_to_num_list(num, num_list):
#     return [x + num for x in num_list]


def add_n(n):
    def helper(num_list):

        for i, item in enumerate(num_list):
            num_list[i] = item + n
        return num_list

        # return [num + n for num in num_list]
    return helper


def multiply(x, y):
    return x * y


if __name__ == '__main__':
    # main()
    # result = multiply(2, 3)
    # print(type(multiply), multiply)

    # print(add_n(10)([1, 5, 3]))
    #
    # add_number_to_num_list = add_n(10)
    # print(type(add_number_to_num_list), add_number_to_num_list)
    #
    # print(add_number_to_num_list([1, 5, 3]))

    for x in range(1, 5):
        for y in range(1, x + 1):
            print(x * 2, end=" ")
        print("")

'''




'''
