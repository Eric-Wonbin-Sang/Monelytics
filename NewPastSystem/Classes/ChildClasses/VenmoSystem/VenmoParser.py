import os
import time
import glob
import pickle
import calendar
import datetime
import dateutil
from bs4 import BeautifulSoup
from selenium import webdriver
from dateutil import relativedelta
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from NewPastSystem.Classes.ParentClasses import Parser

from General import Functions, Constants


class VenmoParser:

    login_url = "https://venmo.com/account/sign-in"
    temp_download_dir = Constants.temp_download_dir
    base_url = "https://venmo.com"
    statement_url = base_url + "/account/statement"
    current_statement_csv_name = Constants.current_statement_file_name_default

    def __init__(self, parent_bank, cookies_path):

        self.parent_bank = parent_bank
        self.cookies_path = cookies_path

        self.driver = None
        self.init_account_dict_list = None
        self.account_dict_list = None
        self.account_list = None

    def login(self):
        self.driver.get(self.login_url)
        while self.driver.current_url == self.login_url:

            username_box = self.driver.find_element_by_name("phoneEmailUsername")
            username_box.clear()
            username_box.send_keys(self.parent_bank.username)

            password_box = self.driver.find_element_by_name("password")
            password_box.clear()
            password_box.send_keys(self.parent_bank.password)
            password_box.send_keys(Keys.RETURN)
            time.sleep(2)

    def get_curr_balance(self):
        time.sleep(1)
        while True:
            try:
                element = self.driver.find_element_by_class_name("balanceTransfer_container__2PLEx")
                if element.text.strip():
                    curr_balance = element.text.strip().split(" ")[0][1:]
                    if float(curr_balance) >= 0:
                        return float(curr_balance)
            except:
                pass

    def get_account_dict_list(self):
        account_dict_list = []

        curr_balance = self.get_curr_balance()

        profile_id, temp_type = self.get_profile_id_and_type()

        name = "Venmo Account"
        nickname = None
        account_type = "debit"
        specific_type = temp_type
        account_number = profile_id
        routing_number_dict = None
        opened_date = None
        account_url = self.driver.current_url

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

    def get_profile_id_and_type(self):

        while True:
            self.driver.get(self.statement_url)
            time.sleep(2)
            try:
                if "Sorry, an error occurred." in self.driver.find_element_by_class_name("p_twenty_l").text:
                    continue
            except:
                break

        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        download_href = soup.findAll("a", {"class": "button button-second1 download-csv"})[0]["href"]
        profile_id = None
        account_type = None
        for part in download_href.split("&"):
            if (profile_id_tag := "profileId=") in part:
                profile_id = part[len(profile_id_tag):]
            if (account_type_tag := "accountType=") in part:
                account_type = part[len(account_type_tag):]
        return profile_id, account_type

    def get_base_download_url(self):
        return self.base_url + "/transaction-history/statement?startDate={start_date}&endDate={end_date}" + \
               "&profileId={}".format(self.account_list[0].account_number) + \
               "&accountType={}".format(self.account_list[0].specific_type)

    def get_start_end_date_tuple_list(self):
        """ returns [(08-01-2020, 08-25-2020), (07-01-2020, 07-31-2020), ...] """
        tuple_list = []
        curr_time = datetime.datetime.now()
        for i in range(int(12 * 6)):
            base_date_str = curr_time.strftime("%m-{}-%Y")
            start_date_str = base_date_str.format("01")
            if i == 0:
                end_date_str = base_date_str.format(curr_time.strftime("%d"))
            else:
                last_day_of_month = calendar.monthrange(curr_time.year, curr_time.month)[1]
                end_date_str = base_date_str.format(str(last_day_of_month).rjust(2, "0"))
            tuple_list.append((start_date_str, end_date_str))
            curr_time = curr_time - dateutil.relativedelta.relativedelta(months=1)
        return tuple_list

    def download_statements(self):

        base_download_url = self.get_base_download_url()

        download_url_list = []
        for start_date_str, end_date_str in self.get_start_end_date_tuple_list():
            download_url_list.append(base_download_url.format(start_date=start_date_str, end_date=end_date_str))
            print("Download url:", download_url_list[-1])

        account = self.account_list[0]

        if self.current_statement_csv_name in os.listdir(account.statement_source_files_path):
            os.remove(account.statement_source_files_path + "/" + self.current_statement_csv_name)

        for i, (start_date_str, end_date_str) in enumerate(self.get_start_end_date_tuple_list()):
            download_url = base_download_url.format(start_date=start_date_str, end_date=end_date_str)
            print(start_date_str, end_date_str, "   ", end="")

            new_csv_name = "{} to {}.csv".format(start_date_str, end_date_str)
            if i == 0:
                new_csv_name = self.current_statement_csv_name
            new_cvs_path = account.statement_source_files_path + "/" + new_csv_name

            if not os.path.exists(new_cvs_path):
                print(download_url, end=" - ")
                for _ in range(4):
                    self.driver.get(download_url)
                    csv_path = Functions.wait_for_temp_file(self.temp_download_dir, 4)
                    if csv_path:
                        os.rename(csv_path, new_cvs_path)
                        break
                print(new_cvs_path, "created!")
            else:
                print(new_cvs_path, "exists!")

    def update_statements(self):
        self.driver = Parser.get_driver(self.temp_download_dir)
        self.login()
        self.account_dict_list = self.get_account_dict_list()

        for account_dict in self.account_dict_list:
            print(account_dict)

        self.account_list = Parser.get_account_list(self.account_dict_list, self.parent_bank)
        self.download_statements()
        self.driver.quit()
