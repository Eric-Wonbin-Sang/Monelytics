import mintapi
import pandas
import pprint
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from General import Functions, Constants

# pandas.set_option('display.max_columns', None)
pandas.options.display.max_columns = None
pandas.options.display.max_seq_items = None
pretty = pprint.PrettyPrinter()


def get_driver(startup_url=None, cookies_path=None, detach=True, run_in_background=False):
    options = Options()

    # if startup_url:
    #     options.add_argument("--app={}".format(startup_url))

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


def save_transaction_df(transaction_df_path):

    mint_login_json = Constants.secrets_dir + "/Monelytics/mint_login.json"
    mint_login_dict = json.load(open(mint_login_json))

    mint = mintapi.Mint(
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

    # accounts = mint.get_accounts(True)
    # for account in accounts:
    #     # mint.get_transactions_csv(id=account["id"])
    #     print(account)
    #     print(mint.get_transactions_json(id=account["id"]))
    #     print("\n----------------------\n")
    #
    # exit()
    Functions.pickle_this(mint.get_transactions(), transaction_df_path)


class Account:

    def __init__(self):
        pass


class Transaction:

    def __init__(self, **kwargs):

        self.init_kwargs = kwargs

        self.date = kwargs.get("date")
        self.description = kwargs.get("description")
        self.original_description = kwargs.get("original_description")
        self.amount = kwargs.get("amount")
        self.transaction_type = kwargs.get("transaction_type")
        self.category = kwargs.get("category")
        self.account_name = kwargs.get("account_name")
        self.labels = kwargs.get("labels")
        self.notes = kwargs.get("notes")

    def __str__(self):
        return " | ".join(
            [
                Functions.str_to_length(self.date, 10, do_dots=False),
                Functions.str_to_length(self.account_name, 19, do_dots=False),
                # Functions.str_to_length(self.amount, 7, do_dots=True),
                str(self.amount).center(7),
                # Functions.str_to_length(self.description, 24, do_dots=True),
                # Functions.str_to_length(self.original_description, 24, do_dots=True),
                str(self.init_kwargs)
            ]
        )


def main():

    transaction_df_path = Constants.project_dir + "/PastSystem/Mint/transaction_df.p"

    save_transaction_df(transaction_df_path=transaction_df_path)
    transaction_df = Functions.unpickle(transaction_df_path)

    transaction_list = []
    for i, row in reversed(list(transaction_df.iterrows())):
        transaction_list.append(Transaction(**{col: row[col] for col in transaction_df.columns}))
        print(transaction_list[-1])


main()
