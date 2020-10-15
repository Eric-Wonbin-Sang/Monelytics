import time
import os
from selenium.webdriver.common.keys import Keys

from PastSystem.Banks.AbstractSystem import UpdateBot
from PastSystem.Banks.Venmo import VenmoAccount

from General import Functions


class VenmoUpdateBot(UpdateBot.UpdateBot):

    def __init__(self, bank_folder_dir):

        super().__init__(
            bank_folder_dir=bank_folder_dir,
            bank_type="Venmo"
        )

    def login(self):
        while self.driver.current_url == self.login_url:
            self.driver.get(self.login_url)
            self.driver.find_element_by_name("phoneEmailUsername").send_keys(self.bank.profile_dict["username"])
            self.driver.find_element_by_name("password").send_keys(self.bank.profile_dict["password"])
            time.sleep(1)
            self.driver.find_element_by_name("password").send_keys(Keys.RETURN)
            time.sleep(2)

    def download_statements(self):

        info_dict = {
            "name": "Personal Account",
            "account_type": "personal"
        }

        if self.bank.abstract_account_list:
            account = self.bank.abstract_account_list[0]
            account_folder_dir = account.account_folder_dir
        else:
            account_folder_dir = self.bank.bank_folder_dir + "/Account - 0"
            os.mkdir(account_folder_dir)
            Functions.dict_to_json(info_dict, account_folder_dir + "/info.json")

        return [
            VenmoAccount.VenmoAccount(
                parent_bank=self,
                driver=self.driver,
                info_dict=info_dict,
                account_folder_dir=account_folder_dir
            )
        ]
