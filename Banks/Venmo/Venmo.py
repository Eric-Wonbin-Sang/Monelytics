import time
import csv
import os
from selenium.webdriver.common.keys import Keys

from Banks.Venmo import VenmoAccount, VenmoStatement
from Banks.Generic import Bank

from General import Constants


class Venmo(Bank.Bank):

    def __init__(self, profile, do_download):

        super().__init__(
            profile=profile,
            login_url="https://venmo.com/account/sign-in",
            login_cookies_pkl=Constants.venmo_login_cookies_pkl,
            do_download=do_download
        )

    def get_driver(self, detach=True, run_in_background=True):
        return super().get_driver(detach, run_in_background)

    def login(self):
        self.driver.find_element_by_name("phoneEmailUsername").send_keys(self.profile.username)
        self.driver.find_element_by_name("password").send_keys(self.profile.password)
        self.driver.find_element_by_name("password").send_keys(Keys.RETURN)
        time.sleep(2)

    def get_account_list(self):
        return [
            VenmoAccount.VenmoAccount(
                parent_bank=self,
                driver=self.driver,
                source_info_dir=self.source_info_dir,
                do_download=self.do_download
            )
        ]
