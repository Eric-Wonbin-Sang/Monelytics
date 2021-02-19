import os
import time
import pickle
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from NewPastSystem.Classes.ParentClasses import Account


class BofAParser:

    login_url = "https://www.bankofamerica.com/"
    auth_url = "https://secure.bankofamerica.com/login/sign-in/entry/signOnV2.go"

    def __init__(self, bofa_bank, cookies_path):

        self.bofa_bank = bofa_bank
        self.cookies_path = cookies_path    # doesn't need it after you remember the comp

        self.driver = self.get_driver()
        self.login()
        self.account_dict_list = self.get_account_dict_list()
        self.account_list = self.get_account_list()

    def get_driver(self):
        options = Options()
        options.add_argument("window-size={},{}".format(1280, 1000))
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        if self.cookies_path and os.path.exists(self.cookies_path):
            for cookie in pickle.load(open(self.cookies_path, "rb")):
                driver.add_cookie(cookie)
        return driver

    def login(self):
        self.driver.get(self.login_url)
        self.driver.find_element_by_name("onlineId1").send_keys(self.bofa_bank.username)
        time.sleep(1)
        self.driver.find_element_by_name("passcode1").send_keys(self.bofa_bank.password)
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

        # if os.path.exists(self.cookies_path):
        #     os.remove(self.cookies_path)
        # pickle.dump(driver.get_cookies(), open(self.cookies_path, "wb"))

    def get_account_dict_list(self):
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
                    "account_url": "https://secure.bankofamerica.com" + list_elem.get("href")
                }
            )
        return account_dict_list

    def get_account_list(self):
        account_list = []

        for account_dict in self.account_dict_list:

            name = account_dict["name"]

            if account_dict["account_type"] == "Checking":
                account_type = "debit"
            elif account_dict["account_type"] == "Liability":
                account_type = "credit"
            else:
                account_type = None

            self.driver.get(account_dict["account_url"])
            self.driver.find_element_by_name("Information_Services").click()

            try:
                nickname = self.driver.find_element_by_class_name("nickname").text
            except:
                nickname = None
            try:
                specific_type = self.driver.find_element_by_class_name("TL_NPI_AcctName").text
            except:
                specific_type = None
            try:
                if account_type == "debit":
                    self.driver.find_element_by_name("show_account_number").click()
                    account_number = self.driver.find_element_by_class_name("TL_NPI_AcctNum").text
                elif account_type == "credit":
                    self.driver.find_element_by_name("acc-num-show").click()
                    account_number = self.driver.find_element_by_id("acctShow").text.split(" ")[0]
                else:
                    account_number = None
            except:
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
            account_list.append(
                Account.Account(
                    parent_bank=self.bofa_bank,
                    **{
                        "name": name,
                        "nickname": nickname,
                        "type": account_type,
                        "specific_type": specific_type,
                        "account_number": account_number,
                        "routing_number_dict": routing_number_dict,
                        "opened_date": opened_date
                    }
                )
            )
        return account_list

    def download_statements(self):
        # if account := self.try_get_account(info_dict):
        #     account_folder_dir = account.account_folder_dir
        # else:
        #     account_folder_dir = self.get_new_account_folder_dir()
        #     os.mkdir(account_folder_dir)
        #     Functions.dict_to_json(info_dict, account_folder_dir + "/info.json")
        #
        # BankOfAmericaAccount.BankOfAmericaAccount(
        #     parent_bank=self,
        #     driver=self.driver,
        #     info_dict=info_dict,
        #     account_folder_dir=account_folder_dir
        # )
        pass
