
from NewPastSystem.Classes.ParentClasses import Bank
from General import Functions, Constants


def main():

    bank_dict_list = Functions.parse_json(Constants.master_logins_json)

    bank_list = Bank.get_bank_list(bank_dict_list)

    for bank in bank_list:
        print(bank)


if __name__ == '__main__':
    main()
