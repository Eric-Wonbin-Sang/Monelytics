import glob
import datetime
import os
from selenium.webdriver import ActionChains
import time

from Banks.Generic import Account
from Banks.BankOfAmerica import BankOfAmericaStatement


class BankOfAmericaAccount(Account.Account):

    def __init__(self, parent_bank, driver, name, account_type, source_info_dir, statement_suffix_url, do_download):

        self.type = account_type

        super().__init__(
            parent_bank=parent_bank,
            driver=driver,
            name=name,
            source_info_dir=source_info_dir,
            base_url="https://secure.bankofamerica.com",
            statement_suffix_url=statement_suffix_url,
            default_statement_csv_name="stmt.csv",
            do_download=do_download
        )

        if self.do_download:
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

    def get_statement_list(self):
        return [
            BankOfAmericaStatement.BankOfAmericaStatement(
                parent_account=self,
                file_name=file_name,
                source_directory=self.download_dir
            ) for file_name in os.listdir(self.download_dir)
        ]
