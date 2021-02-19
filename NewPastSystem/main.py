
from NewPastSystem.Classes.ParentClasses import Bank
from NewPastSystem.Classes.ChildClasses import BofA

from General import Functions, Constants


def get_bank_list(bank_dict_list):
    bank_list = []
    for bank_dict in bank_dict_list:
        bank_type = bank_dict.get("bank_type")
        if bank_type == "Bank of America":
            bank_list.append(BofA.BofA(**bank_dict))
        elif bank_type == "Discover":
            bank_list.append(Bank.Bank(**bank_dict))
        elif bank_type == "Chase":
            bank_list.append(Bank.Bank(**bank_dict))
        elif bank_type == "Venmo":
            bank_list.append(Bank.Bank(**bank_dict))
        elif bank_type == "Mint":
            bank_list.append(Bank.Bank(**bank_dict))
        else:
            print("unknown bank type:", bank_type)
    return bank_list


def main():

    bank_dict_list = Functions.parse_json(Constants.master_logins_json)

    bank_list = get_bank_list(bank_dict_list)

    for bank in bank_list:
        print(bank)


if __name__ == '__main__':
    main()
