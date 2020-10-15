import time
import os
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

from PastSystem.Banks.AbstractSystem import UpdateBot
from PastSystem.Banks.BankOfAmerica import BankOfAmericaAccount

from General import Functions


class BankOfAmericaUpdateBot(UpdateBot.UpdateBot):

    def __init__(self, bank_folder_dir):

        super().__init__(
            bank_folder_dir=bank_folder_dir,
            bank_type="Bank Of America"
        )

    def login(self):
        self.driver.find_element_by_name("onlineId1").send_keys(self.bank.profile_dict["username"])
        self.driver.find_element_by_name("passcode1").send_keys(self.bank.profile_dict["password"])
        self.driver.find_element_by_id("signIn").send_keys(Keys.RETURN)
        time.sleep(2)

    def try_get_account(self, info_dict):
        """ This returns an existing abstract account with a similar info_dict. """
        for account in self.bank.abstract_account_list:
            if account.info_dict["name"] == info_dict["name"] and \
                    account.info_dict["account_type"] == info_dict["account_type"]:
                return account
        return None

    def get_account_dir_list(self):
        return [
            path for path in Functions.get_path_list_in_dir(self.bank.bank_folder_dir)
            if "Account" == path.split("/")[-1].split(" - ")[0]
        ]

    def get_new_account_folder_dir(self):
        num_list = [int(path.split("/")[-1].split(" - ")[-1]) for path in self.get_account_dir_list()]
        num = 0
        while True:
            if num not in num_list:
                break
            num += 1
        return self.bank.bank_folder_dir + "/Account - {}".format(num)

    def download_statements(self):
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        account_elem_list = soup.findAll("div", {"class": "AccountItem AccountItemDeposit"})
        for i, account_elem in enumerate(account_elem_list):
            account_name_elem = account_elem.findAll("span", {"class": "AccountName"})[0]
            list_elem = account_name_elem.findAll("a")[0]

            info_dict = {
                "name": list_elem.text,
                "account_type": account_elem.get("data-accounttype")
            }

            if account := self.try_get_account(info_dict):
                account_folder_dir = account.account_folder_dir
            else:
                account_folder_dir = self.get_new_account_folder_dir()
                os.mkdir(account_folder_dir)
                Functions.dict_to_json(info_dict, account_folder_dir + "/info.json")

            BankOfAmericaAccount.BankOfAmericaAccount(
                parent_bank=self,
                driver=self.driver,
                info_dict=info_dict,
                account_folder_dir=account_folder_dir
            )
