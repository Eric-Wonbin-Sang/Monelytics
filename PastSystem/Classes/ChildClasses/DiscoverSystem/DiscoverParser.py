import os
import time
from selenium.webdriver.common.keys import Keys

from PastSystem.Classes.ParentClasses import Parser

from General import Functions


class DiscoverParser:

    login_url = "https://portal.discover.com/customersvcs/universalLogin/ac_main"
    # auth_url = "https://secure.bankofamerica.com/login/sign-in/entry/signOnV2.go"
    curr_statement_name_segment = "Discover-Recent"

    def __init__(self, parent_bank, cookies_path):

        self.parent_bank = parent_bank
        self.cookies_path = cookies_path  # doesn't need it after you remember the comp

        self.driver = None
        self.init_account_dict_list = None
        self.account_dict_list = None
        self.account_list = None

    def login(self):
        self.driver.get(self.login_url)
        while self.driver.current_url == self.login_url:
            username_box = self.driver.find_element_by_id("userid-content")
            username_box.clear()
            username_box.send_keys(self.parent_bank.username)
            password_box = self.driver.find_element_by_id("password-content")
            password_box.clear()
            password_box.send_keys(self.parent_bank.password)
            password_box.send_keys(Keys.RETURN)

    def get_curr_balance(self):
        while True:
            try:
                return float(self.driver.find_element_by_class_name("current-balance-value").text)
            except:
                pass

    def get_account_dict_list(self):
        curr_balance = self.get_curr_balance()
        self.driver.get("https://card.discover.com/cardmembersvcs/statements/app/activity#/recent")
        time.sleep(.1)
        while True:
            try:
                self.driver.find_element_by_class_name("activity-period").click()
                break
            except:
                pass

        account_dict_list = []
        show_account_button = self.driver.find_elements_by_class_name("right-link")[-1]
        show_account_button.click()
        name = self.driver.find_elements_by_class_name("card-name")[1].text

        url_list = [x.get_attribute("href") for x in self.driver.find_elements_by_class_name("right-link")]
        homepage_url = url_list[0]
        help_center_url = url_list[1]
        profile_url = url_list[2]

        self.driver.get(profile_url)

        text_list = [str(x.text) for x in self.driver.find_elements_by_class_name("glassbox-masked")]
        account_number = text_list[7]

        account_dict_list.append(
            {
                "name": name,
                "nickname": None,
                "type": "credit",
                "specific_type": None,
                "curr_balance": curr_balance,
                "account_number": account_number,
                "routing_number_dict": {
                    "paper": None,
                    "electronic": None,
                    "wire": None
                },
                # "opened_date": self.opened_date,
                "account_url": self.driver.current_url
            }
        )
        return account_dict_list

    def get_download_statement_button(self):
        for button in self.driver.find_elements_by_class_name("btn-primary"):
            if button.get_attribute("value") == "Download":
                return button

    def try_statement_download(self):
        print("Attempting to download statement...", end="")
        self.driver.find_element_by_id("submitDownload").click()
        print("Waiting for csv...", end="")
        return Functions.wait_for_temp_file(self.parent_bank.profile.temp_download_dir, 2)

    def find_curr_statement_path(self, account):
        for path in os.listdir(account.statement_source_files_dir):
            if self.curr_statement_name_segment in path:
                return path

    def download_statements(self):
        self.driver.get("https://card.discover.com/cardmembersvcs/statements/app/activity#/recent")
        time.sleep(.1)
        while True:
            try:
                self.driver.find_element_by_class_name("activity-period").click()
                break
            except:
                pass

        period_url_list = []
        container_list = self.driver.find_element_by_id("statementList").find_elements_by_class_name("date-container")
        for container in container_list:
            period_url = container.find_elements_by_css_selector("*")[0].get_attribute("href")
            print(container.text, period_url)
            period_url_list.append(period_url)

        for account in self.account_list:

            current_statement_path = self.find_curr_statement_path(account)
            if current_statement_path in os.listdir(account.statement_source_files_dir):
                os.remove(account.statement_sorce_files_path + "/" + current_statement_path)

            for period_url in period_url_list:
                self.driver.get(period_url)
                while True:
                    try:
                        download_modal_button = self.driver.find_element_by_class_name("download-link")
                        download_modal_button.click()
                        break
                    except:
                        time.sleep(.1)
                self.driver.find_element_by_css_selector("input[type='radio'][name='outputFormat'][id='radio4'][value='csv']").click()
                csv_path = self.try_statement_download()
                self.driver.find_element_by_css_selector("a[class='link modal-close-link']").click()

                new_path = account.statement_source_files_dir + "/" + csv_path.replace("\\", "/").split("/")[-1]
                print(new_path + " - ", end="")
                if not os.path.exists(new_path):
                    os.rename(csv_path, new_path)
                    print(new_path, "created!")
                else:
                    print(new_path, "exists!")
                    os.remove(csv_path)

    def update_statements(self):
        self.driver = Parser.get_driver(self.parent_bank.profile.temp_download_dir)
        self.login()
        self.account_dict_list = self.get_account_dict_list()

        for account_dict in self.account_dict_list:
            print(account_dict)

        self.account_list = Parser.get_account_list(self.account_dict_list, self.parent_bank)
        self.download_statements()
        self.driver.quit()
