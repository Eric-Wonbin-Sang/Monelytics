import time
from selenium.webdriver import ActionChains

from PastSystem.Classes.ParentClasses import Parser



class ChaseParser:

    login_url = "https://secure05c.chase.com/web/auth/dashboard"
    auth_url = "https://secure05c.chase.com/web/auth/dashboard#/dashboard/overviewAccounts/overview/index"
    success_url = "https://secure03b.chase.com/web/auth/dashboard#/dashboard/overviewAccounts/overview/multiProduct"
    # current_debit_statement_csv_name = "Current transactions.csv"
    # current_credit_statement_csv_name = "transaction_period.csv"

    def __init__(self, parent_bank, cookies_path):

        self.parent_bank = parent_bank
        self.cookies_path = cookies_path    # doesn't need it after you remember the comp

        self.driver = None
        self.init_account_dict_list = None
        self.account_dict_list = None
        self.account_list = None

    def update_statements(self):
        self.driver = Parser.get_driver(self.parent_bank.profile.temp_download_dir)
        self.login()
        self.init_account_dict_list = self.get_init_account_dict_list()
        self.account_dict_list = self.get_account_dict_list()

        self.account_list = Parser.get_account_list(self.account_dict_list, self.parent_bank)
        self.download_statements()
        self.driver.quit()

    def login(self):
        self.driver.get("https://www.google.com/")
        self.driver.get(self.login_url)
        time.sleep(2)
        ActionChains(self.driver).send_keys(self.parent_bank.username).perform()
        ActionChains(self.driver).send_keys("\t").perform()
        ActionChains(self.driver).send_keys(self.parent_bank.password).perform()
        ActionChains(self.driver).send_keys("\n").perform()

        while self.driver.current_url == self.auth_url:
            time.sleep(.2)

    def get_account_dict_list(self):

        account_dict_list = []

        # for account_div in self.driver.find_elements_by_css_selector("div[class='accounts-blade util clearfix']"):
        #     account_type = "credit" if "credit" in account_div.text.lower() else "debit"
        #
        #     if account_type == "debit":
        #         name = account_div.find_element_by_
        #
        #     else:
        #
        #
        #     account_dict_list.append(
        #         {
        #             "name": name,
        #             "nickname": nickname,
        #             "type": account_type,
        #             "specific_type": specific_type,
        #             "curr_balance": curr_balance,
        #             "account_number": account_number,
        #             "routing_number_dict": routing_number_dict,
        #             "opened_date": opened_date,
        #             "account_url": account_url
        #         }
        #     )

        return account_dict_list
