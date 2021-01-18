import os
import json
import pandas
import pprint
import mintapi
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from PastSystem.Mint.Classes.Transaction import Transaction
from PastSystem.Mint.Classes.Account import Account

from General import Functions, Constants

# pandas.set_option('display.max_columns', None)
pandas.options.display.max_columns = None
pandas.options.display.max_seq_items = None
pretty = pprint.PrettyPrinter()


def get_driver(startup_url=None, cookies_path=None, detach=True, run_in_background=False):
    options = Options()
    options.add_argument("window-size={},{}".format(1280, 1000))
    options.add_experimental_option("detach", detach)
    # if run_in_background:
    #     options.add_argument('--disable-gpu')
    #     options.add_argument('--disable-software-rasterizer')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    # if cookies_path and os.path.exists(cookies_path):
    #     for cookie in pickle.load(open(cookies_path, "rb")):
    #         driver.add_cookie(cookie)
    driver.get(startup_url)
    return driver


def get_mint(mint_login_json):

    mint_login_dict = json.load(open(mint_login_json))

    return mintapi.Mint(
        mint_login_dict["username"],
        mint_login_dict["password"],
        mfa_method='sms',
        headless=True,
        mfa_input_callback=None,
        session_path=None,
        imap_account=None,
        imap_password=None,
        imap_server=None,
        imap_folder='INBOX',
        wait_for_sync=False,
        wait_for_sync_timeout=300
    )


def update_mint(mint_login_json, transaction_df_path, account_save_dir):
    mint = get_mint(mint_login_json)
    Functions.pickle_this(mint.get_transactions(), transaction_df_path)
    for account_dict in mint.get_accounts(True):
        temp_account = Account(account_dict)
        Functions.pickle_this(temp_account, account_save_dir + "/" + temp_account.get_save_filename())


def get_transaction_df(transaction_df_path):
    return Functions.unpickle(transaction_df_path)


def get_transaction_list(transaction_df):
    transaction_list = []
    for i, row in reversed(list(transaction_df.iterrows())):
        transaction_list.append(Transaction(**{col: row[col] for col in transaction_df.columns}))
    return transaction_list


def get_account_list(save_dir):
    return [Functions.unpickle(save_dir + "/" + path) for path in os.listdir(save_dir)]


def main():

    mint_login_json = Constants.secrets_dir + "/Monelytics/Mint/mint_login.json"
    transaction_df_path = Constants.secrets_dir + "/Monelytics/Mint/transaction_df.p"
    account_save_dir = Constants.secrets_dir + "/Monelytics/Mint/Accounts"

    update = False

    if update:
        update_mint(
            mint_login_json=mint_login_json,
            transaction_df_path=transaction_df_path,
            account_save_dir=account_save_dir
        )

    transaction_df = get_transaction_df(transaction_df_path)
    transaction_list = get_transaction_list(transaction_df)
    account_list = get_account_list(Constants.secrets_dir + "/Monelytics/Mint/Accounts")

    for account in account_list:
        print(account)

    for transaction in transaction_list:
        # if transaction.amount > 1000:
        print(transaction)


main()
