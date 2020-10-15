import glob
import datetime
import os
from selenium.webdriver import ActionChains
import time

from General import Constants


class BankOfAmericaAccount:

    def __init__(self, parent_bank, driver, info_dict, account_folder_dir):

        self.parent_bank = parent_bank
        self.driver = driver
        self.info_dict = info_dict
        self.account_folder_dir = account_folder_dir

        self.user_download_dir = Constants.user_download_dir
        self.base_url = "https://secure.bankofamerica.com"
        self.default_statement_csv_name = "stmt.csv"
        self.current_statement_csv_name = Constants.current_statement_file_name_default
        self.statement_url = self.base_url + self.info_dict["statement_suffix_url"]

        self.download_and_store()

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

    def download_and_store(self):
        self.driver.get(self.statement_url)
        self.click_download_transactions_elem()
        self.change_file_type_to_excel()

        if self.current_statement_csv_name in os.listdir(self.account_folder_dir):
            os.remove(self.account_folder_dir + "/" + self.current_statement_csv_name)

        option_list = self.get_time_period_option_elem_list()
        for i in range(len(option_list)):
            (option := option_list[i]).click()
            period_name = option.get_attribute("value").strip().replace("/", ".")
            print(period_name + " - ", end="")
            if not os.path.exists(self.account_folder_dir + "/" + (csv_name := period_name + ".csv")):
                csv_path = self.try_download_and_get_csv_path()
                new_path = self.account_folder_dir + "/" + csv_name
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
                print(self.account_folder_dir + "/" + csv_name, "exists!")
