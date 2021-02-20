import os

from NewPastSystem.Classes.ParentClasses import Bank
from NewPastSystem.Classes.ChildClasses.BofASystem import BofABank

from General import Functions, Constants


type_to_bank_class_dict = {
    "Bank of America": BofABank.BofABank,
    "Discover": Bank.Bank,
    "Chase": Bank.Bank,
    "Venmo": Bank.Bank,
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


def main():

    existing_bank_list = get_existing_bank_list(Constants.banks_dir)
    bank_dict_list = Functions.parse_json(Constants.bank_logins_json)
    new_bank_list = get_bank_list(bank_dict_list, existing_bank_list)

    bank_list = existing_bank_list + new_bank_list
    for bank in bank_list:
        print(bank)


if __name__ == '__main__':
    main()
