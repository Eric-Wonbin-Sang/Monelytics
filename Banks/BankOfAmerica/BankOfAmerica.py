import time
import os
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

from Banks.Generic import Bank
from Banks.BankOfAmerica import BankOfAmericaAccount

from General import Constants


class BankOfAmerica(Bank.Bank):

    def __init__(self, profile, do_download):

        super().__init__(
            profile=profile,
            login_url="https://www.bankofamerica.com/",
            login_cookies_pkl=Constants.bofa_login_cookies_pkl,
            do_download=do_download
        )

    def login(self):
        self.driver.find_element_by_name("onlineId1").send_keys(self.profile.username)
        self.driver.find_element_by_name("passcode1").send_keys(self.profile.password)
        self.driver.find_element_by_id("signIn").send_keys(Keys.RETURN)
        time.sleep(2)

    def get_account_list(self):
        account_list = []
        if self.do_download:
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            account_elem_list = soup.findAll("div", {"class": "AccountItem AccountItemDeposit"})
            for account_elem in account_elem_list:
                account_name_elem = account_elem.findAll("span", {"class": "AccountName"})[0]
                list_elem = account_name_elem.findAll("a")[0]
                account_list.append(
                    BankOfAmericaAccount.BankOfAmericaAccount(
                        parent_bank=self,
                        driver=self.driver,
                        name=list_elem.text,
                        source_info_dir=self.source_info_dir,
                        account_type=account_elem.get("data-accounttype"),
                        statement_suffix_url=list_elem["href"],
                        do_download=self.do_download
                    )
                )
        else:
            for account_data_folder_name in os.listdir(self.source_info_dir):
                account_list.append(
                    BankOfAmericaAccount.BankOfAmericaAccount(
                        driver=self.driver,
                        parent_bank=self,
                        name=account_data_folder_name,
                        source_info_dir=self.source_info_dir,
                        account_type=None,
                        statement_suffix_url=None,
                        do_download=self.do_download
                    )
                )
        return account_list
