import os
import time
import pickle
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from NewPastSystem.Classes.ParentClasses import Account

from General import Functions, Constants


class BofAParser:

    login_url = "https://www.bankofamerica.com/"
    auth_url = "https://secure.bankofamerica.com/login/sign-in/entry/signOnV2.go"
    temp_download_dir = Constants.temp_download_dir
    current_debit_statement_csv_name = "Current transactions.csv"
    current_credit_statement_csv_name = "transaction_period.csv"

    def __init__(self, bofa_bank, cookies_path):

        self.bofa_bank = bofa_bank
        self.cookies_path = cookies_path    # doesn't need it after you remember the comp

        self.driver = None
        self.init_account_dict_list = None
        self.account_dict_list = None
        self.account_list = None

    def update_statements(self):
        self.driver = self.get_driver()
        self.login()
        self.init_account_dict_list = self.get_init_account_dict_list()
        self.account_dict_list = self.get_account_dict_list()

        self.account_list = self.get_account_list()
        self.download_statements()
        self.driver.quit()

    def get_driver(self):
        options = Options()
        options.add_argument("window-size={},{}".format(1280, 1000))

        prefs = {"download.default_directory": Constants.temp_download_dir}
        options.add_experimental_option("prefs", prefs)

        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        if self.cookies_path and os.path.exists(self.cookies_path):
            for cookie in pickle.load(open(self.cookies_path, "rb")):
                driver.add_cookie(cookie)
        return driver

    def login(self):
        self.driver.get(self.login_url)
        while self.driver.current_url == self.login_url:
            username_box = self.driver.find_element_by_name("onlineId1")
            username_box.clear()
            username_box.send_keys(self.bofa_bank.username)
            time.sleep(1)
            password_box = self.driver.find_element_by_name("passcode1")
            password_box.clear()
            password_box.send_keys(self.bofa_bank.password)
            self.driver.find_element_by_id("signIn").send_keys(Keys.RETURN)
            time.sleep(2)

        # set up two factor authentication (only requires it once)
        while self.driver.current_url == self.auth_url:
            send_code_button = self.driver.find_element_by_id("btnARContinue")
            send_code_button.send_keys(Keys.RETURN)

            auth_code = input("Please input two factor auth code: ")

            auth_code_box = self.driver.find_element_by_id("tlpvt-acw-authnum")
            auth_code_box.clear()
            auth_code_box.send_keys(auth_code)

            recognize_computer_radio = self.driver.find_element_by_id("yes-recognize")
            recognize_computer_radio.click()

            submit_button = self.driver.find_element_by_id("continue-auth-number")
            submit_button.send_keys(Keys.RETURN)

    def get_init_account_dict_list(self):
        account_dict_list = []
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        account_elem_list = soup.findAll("div", {"class": "AccountItem"})
        for i, account_elem in enumerate(account_elem_list):
            account_name_elem = account_elem.findAll("span", {"class": "AccountName"})[0]
            list_elem = account_name_elem.findAll("a")[0]
            account_dict_list.append(
                {
                    "name": list_elem.text,
                    "account_type": account_elem.get("data-accounttype"),
                    "account_url": "https://secure.bankofamerica.com" + list_elem.get("href"),
                    "curr_balance": float(account_elem.find("span", {"class": "balanceValue TL_NPI_L1"}).text[1:].replace(",", ""))
                }
            )
        return account_dict_list

    def get_account_dict_list(self):
        account_dict_list = []
        for init_account_dict in self.init_account_dict_list:

            name = init_account_dict["name"]
            account_url = init_account_dict["account_url"]
            if init_account_dict["account_type"] == "Checking":
                account_type = "debit"
            elif init_account_dict["account_type"] == "Liability":
                account_type = "credit"
            else:
                account_type = None

            curr_balance = init_account_dict["curr_balance"]

            self.driver.get(init_account_dict["account_url"])
            self.driver.find_element_by_name("Information_Services").click()

            try:
                nickname = self.driver.find_element_by_class_name("nickname").text
            except:
                nickname = None
            try:
                specific_type = self.driver.find_element_by_class_name("TL_NPI_AcctName").text
            except:
                specific_type = None

            account_number = None
            try:
                start_time = datetime.datetime.now()

                if account_type == "debit":
                    self.driver.find_element_by_name("show_account_number").click()
                elif account_type == "credit":
                    self.driver.find_element_by_name("acc-num-show").click()
                while (datetime.datetime.now() - start_time).total_seconds() < 10:
                    if account_type == "debit":
                        account_number = self.driver.find_element_by_class_name("TL_NPI_AcctNum").text
                    elif account_type == "credit":
                        account_number = self.driver.find_element_by_id("acctShow").text.split(" ")[0]
                    else:
                        print("ACCOUNT", name, "IS NEITHER DEBIT OR CREDIT")
                        break
                    if account_number != "":
                        break
                    time.sleep(.2)
                else:
                    print("ACCOUNT", name, "ACCOUNT NUMBER PARSE FAILED")
                    account_number = None
            except:
                print("ACCOUNT", name, "ACCOUNT NUMBER PARSE FAILED")
                account_number = None
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            details_row_div_list = soup.findAll("div", {"class": "details-row"})
            try:
                part_list = [part.strip() for part in details_row_div_list[3].text.split("\n") if part.strip() != ""]
                paper, electronic = part_list[1], part_list[2][1:]
            except:
                paper, electronic = None, None
            try:
                wires = details_row_div_list[4].text.strip().split(" ")[0]
            except:
                wires = None
            routing_number_dict = {
                "paper": paper,
                "electronic": electronic,
                "wires": wires
            }
            try:
                opened_date = datetime.datetime.strptime(details_row_div_list[5].text.strip().split("\n")[-1], "%m/%d/%Y")
            except:
                opened_date = None
            account_dict_list.append(
                {
                    "name": name,
                    "nickname": nickname,
                    "type": account_type,
                    "specific_type": specific_type,
                    "curr_balance": curr_balance,
                    "account_number": account_number,
                    "routing_number_dict": routing_number_dict,
                    "opened_date": opened_date,
                    "account_url": account_url
                }
            )
        return account_dict_list

    def get_account_list(self):
        account_list = []
        for account_dict in self.account_dict_list:
            print("THIS", account_dict["curr_balance"])
            if account_dict["account_number"] \
                    in [existing_account.account_number for existing_account in self.bofa_bank.account_list]:

                # ADD LOGIC HERE TO UPDATE ACCOUNT.JSON WITH A TEMP ACCOUNT OBJECT

                continue
            account_list.append(
                Account.Account(
                    parent_bank=self.bofa_bank,
                    dir_name=None,
                    **account_dict
                )
            )
            print("Created Account:", account_list[-1].name, account_list[-1].type)
        return self.bofa_bank.account_list + account_list

    # statement downloading ---------------------------------------------------------------
    def get_debit_download_menu_elem(self):
        return self.driver.find_element_by_name("download_transactions_top")

    def get_credit_download_menu_elem(self):
        count = 0
        while True:
            time_select = Select(self.driver.find_element_by_id("goto_select_trans_bottom"))
            time_select.select_by_index(count)
            try:
                return self.driver.find_element_by_name("download_transactions_top")
            except:
                pass
            count += 1

    def change_file_type_to_excel(self):
        file_type_select = self.driver.find_element_by_id("select_filetype")
        for option in file_type_select.find_elements_by_tag_name("option"):
            if option.text == "Microsoft Excel Format":
                option.click()
                break

    def get_period_option_list(self, option_parent_id, account_type):
        while True:
            option_list = self.driver.find_element_by_id(option_parent_id).find_elements_by_tag_name("option")
            option = option_list[0]
            if option.is_displayed() and option.is_enabled():
                return option_list
            if account_type == "debit":
                ActionChains(self.driver).click(self.get_debit_download_menu_elem()).perform()
            else:
                ActionChains(self.driver).click(self.get_credit_download_menu_elem()).perform()

    def get_debit_download_button_elem(self):
        for elem in self.driver.find_elements_by_tag_name("a"):
            if elem.get_attribute("href") is not None and elem.get_attribute("class") \
                    == "btn-bofa btn-bofa-blue btn-bofa-small submit-download btn-bofa-noRight":
                return elem

    def get_credit_download_button_elem(self):
        for elem in self.driver.find_elements_by_tag_name("a"):
            if elem.get_attribute("href") is not None and elem.get_attribute("class") \
                    == "btn-bofa btn-bofa-small btn-bofa-blue submit-download btn-bofa-noRight":
                return elem

    def try_statement_download(self, download_button_elem):
        print("Attempting to download statement...", end="")
        while True:
            try:
                download_button_elem.click()
                break
            except Exception as e:
                time.sleep(.1)
                print(".", end="")
        print("Waiting for csv...", end="")
        return Functions.wait_for_temp_file(self.temp_download_dir, 2)

    def download_debit_account_statements(self, account):
        ActionChains(self.driver).click(self.get_debit_download_menu_elem()).perform()
        for i in range(len(self.get_period_option_list("select_txnperiod", "debit"))):
            option = self.get_period_option_list("select_txnperiod", "debit")[i]
            option.click()
            self.change_file_type_to_excel()

            period_name = option.get_attribute("value").strip().replace("/", ".")
            csv_name = period_name + ".csv"
            new_path = account.statement_source_files_path + "/" + csv_name
            print(period_name + " - ", end="")
            if not os.path.exists(new_path):
                csv_path = self.try_statement_download(self.get_debit_download_button_elem())
                if csv_path is not None:
                    os.rename(csv_path, new_path)
                    print(new_path, "created!")
                else:
                    open(new_path, "w").close()
                    print(new_path, "created! - empty")
            else:
                print(new_path, "exists!")
            ActionChains(self.driver).click(self.get_debit_download_menu_elem()).perform()

    def download_credit_account_statements(self, account):
        ActionChains(self.driver).click(self.get_credit_download_menu_elem()).perform()
        for i in range(len(self.get_period_option_list("select_transaction", "credit"))):
            option = self.get_period_option_list("select_transaction", "credit")[i]
            option.click()
            self.change_file_type_to_excel()

            period_name = option.get_attribute("name")
            csv_name = period_name + ".csv"
            new_path = account.statement_source_files_path + "/" + csv_name
            print(period_name + " - ", end="")
            if not os.path.exists(new_path):
                csv_path = self.try_statement_download(self.get_credit_download_button_elem())
                os.rename(csv_path, new_path)
                print(new_path, "created!")
            else:
                print(new_path, "exists!")
            ActionChains(self.driver).click(self.get_credit_download_menu_elem()).perform()

    def download_statements(self):
        for account in self.account_list:
            self.driver.get(account.account_url)
            if account.type == "debit":
                if self.current_debit_statement_csv_name in os.listdir(account.statement_source_files_path):
                    os.remove(account.statement_source_files_path + "/" + self.current_debit_statement_csv_name)
                self.download_debit_account_statements(account)
            elif account.type == "credit":
                if self.current_credit_statement_csv_name in os.listdir(account.statement_source_files_path):
                    os.remove(account.statement_source_files_path + "/" + self.current_credit_statement_csv_name)
                self.download_credit_account_statements(account)
