import glob
import datetime
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
import time

from Classes import Bank

from General import Constants


class BankOfAmerica(Bank.Bank):

    def __init__(self, profile):

        super().__init__(
            profile=profile,
            login_url="https://www.bankofamerica.com/",
            login_cookies_pkl=Constants.bofa_login_cookies_pkl
        )

    def login(self):
        self.driver.find_element_by_name("onlineId1").send_keys(self.profile.username)
        self.driver.find_element_by_name("passcode1").send_keys(self.profile.password)
        self.driver.find_element_by_id("signIn").send_keys(Keys.RETURN)
        time.sleep(2)

    def get_account_list(self):
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        account_elem_list = soup.findAll("div", {"class": "AccountItem AccountItemDeposit"})
        account_list = []
        for account_elem in account_elem_list:
            account_name_elem = account_elem.findAll("span", {"class": "AccountName"})[0]
            list_elem = account_name_elem.findAll("a")[0]
            account_list.append(
                Account(
                    name=list_elem.text,
                    type=account_elem.get("data-accounttype"),
                    source_info_dir=self.source_info_dir,
                    redirect_link=list_elem["href"],
                    driver=self.driver
                )
            )
        return account_list


class Account:

    def __init__(self, **kwargs):

        self.driver = kwargs.get("driver")
        self.name = kwargs.get("name")
        self.type = kwargs.get("type")
        self.source_info_dir = kwargs.get("source_info_dir")
        self.redirect_link = "https://secure.bankofamerica.com" + kwargs.get("redirect_link")

        self.download_dir = self.get_download_dir(parent_dir=self.source_info_dir)
        self.user_download_dir = Constants.user_download_dir

        self.default_statement_csv_name = "stmt.csv"
        self.current_statement_csv_name = "Current transactions.csv"
        self.get_transactions()

    def get_download_dir(self, parent_dir):
        download_dir = parent_dir + "/" + self.name
        if not os.path.exists(download_dir):
            os.mkdir(download_dir)
        return download_dir

    def click_download_transactions_elem(self):
        download_menu_button = self.driver.find_element_by_name("download_transactions_top")
        ActionChains(self.driver).click(download_menu_button).perform()
        return download_menu_button

    def change_file_type_to_excel(self):
        file_type_select = self.driver.find_element_by_id("select_filetype")
        for option in file_type_select.find_elements_by_tag_name("option"):
            if option.text == "Microsoft Excel Format":
                option.click()
                break

    def get_download_button_elem(self):
        for elem in self.driver.find_elements_by_tag_name("a"):
            if elem.get_attribute("href") is not None and elem.get_attribute("class") \
                    == "btn-bofa btn-bofa-blue btn-bofa-small submit-download btn-bofa-noRight":
                return elem

    def try_download_and_get_csv_path(self):
        download_button_elem = self.get_download_button_elem()
        print("Attempting to download statement...", end="")
        while True:
            try:
                download_button_elem.click()
                break
            except Exception as e:
                time.sleep(.1)
                print(".", end="")
        print("Waiting for csv...", end="")
        csv_path = None
        base_time = datetime.datetime.now()
        while (datetime.datetime.now() - base_time).seconds < 2:
            if len(csv_list := glob.glob(self.user_download_dir + "/" + self.default_statement_csv_name)) > 0:
                csv_path = csv_list[0]
                break
            print(".", end="")
            time.sleep(.1)
        return csv_path

    def get_time_period_option_elem_list(self):
        return self.driver.find_element_by_id("select_txnperiod").find_elements_by_tag_name("option")

    def get_transactions(self):

        self.driver.get(self.redirect_link)
        self.click_download_transactions_elem()
        self.change_file_type_to_excel()

        if self.current_statement_csv_name in os.listdir(self.download_dir):
            os.remove(self.download_dir + "/" + self.current_statement_csv_name)

        option_list = self.get_time_period_option_elem_list()
        for i in range(len(option_list)):
            (option := option_list[i]).click()
            period_name = option.get_attribute("value").strip().replace("/", ".")
            print(period_name + " - ", end="")
            if not os.path.exists(self.download_dir + "/" + (csv_name := period_name + ".csv")):
                csv_path = self.try_download_and_get_csv_path()
                new_path = self.download_dir + "/" + csv_name
                if csv_path is not None:
                    os.rename(csv_path, new_path)
                    print(new_path, "created!")
                else:
                    open(new_path, "w").close()
                    print(new_path, "created! - empty")
                    self.click_download_transactions_elem()
                    self.change_file_type_to_excel()
                    option_list = self.get_time_period_option_elem_list()
            else:
                print(self.download_dir + "/" + csv_name, "exists!")
