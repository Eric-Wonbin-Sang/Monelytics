from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from PastSystem.Classes.ParentClasses import Account


def get_driver(download_dir):
    options = Options()
    options.add_argument("window-size={},{}".format(1280, 1000))

    prefs = {"download.default_directory": download_dir}
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    return driver


def get_account_list(account_dict_list, parent_bank):
    account_list = []
    for account_dict in account_dict_list:
        if account_dict["account_number"] \
                in [existing_account.account_number for existing_account in parent_bank.account_list]:

            # ADD LOGIC HERE TO UPDATE ACCOUNT.JSON WITH A TEMP ACCOUNT OBJECT

            continue
        account_list.append(
            Account.Account(
                parent_bank=parent_bank,
                dir_name=None,
                **account_dict
            )
        )
        print("Created Account:", account_list[-1].name, account_list[-1].type)
    return parent_bank.account_list + account_list
