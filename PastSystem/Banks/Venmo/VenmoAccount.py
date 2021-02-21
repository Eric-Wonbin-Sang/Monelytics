import datetime
import calendar
import dateutil
import glob
import os
from dateutil import relativedelta
from bs4 import BeautifulSoup
import time

from General import Constants


class VenmoAccount:

    def __init__(self, parent_bank, driver, info_dict, account_folder_dir):

        self.curr_datetime = datetime.datetime.now()

        self.parent_bank = parent_bank
        self.driver = driver
        self.info_dict = info_dict
        self.account_folder_dir = account_folder_dir

        self.user_download_dir = Constants.user_download_dir
        self.base_url = "https://venmo.com"
        self.default_statement_csv_name = "venmo_statement.csv"
        self.current_statement_csv_name = Constants.current_statement_file_name_default
        self.statement_url = self.base_url + "/account/statement"

        self.profile_id, self.type = self.get_profile_id_and_type()
        self.base_download_url = self.get_base_download_url()
        self.start_end_date_tuple_list = self.get_start_end_date_tuple_list()

        self.download_and_store()

    def get_profile_id_and_type(self):
        self.driver.get(self.statement_url)
        time.sleep(2)

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
               "&profileId={}".format(self.profile_id) + "&accountType={}".format(self.type)

    def get_start_end_date_tuple_list(self):
        """ returns [(08-01-2020, 08-25-2020), (07-01-2020, 07-31-2020), ...] """
        tuple_list = []
        curr_time = self.curr_datetime
        for i in range(12):
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

    def download_and_store(self):
        if self.current_statement_csv_name in os.listdir(self.account_folder_dir):
            os.remove(self.account_folder_dir + "/" + self.current_statement_csv_name)

        for i, (start_date_str, end_date_str) in enumerate(self.start_end_date_tuple_list):
            download_url = self.base_download_url.format(start_date=start_date_str, end_date=end_date_str)
            print(start_date_str, end_date_str, "   ", end="")

            if i == 0:
                new_csv_name = self.current_statement_csv_name
            else:
                new_csv_name = "{} to {}.csv".format(start_date_str, end_date_str)
            new_cvs_path = self.account_folder_dir + "/" + new_csv_name

            if not os.path.exists(new_cvs_path):
                self.driver.get(download_url)
                os.rename(Functions.wait_for_temp_file(self.temp_download_dir, 2), new_cvs_path)
                print(new_cvs_path, "created!")
            else:
                print(new_cvs_path, "exists!")
