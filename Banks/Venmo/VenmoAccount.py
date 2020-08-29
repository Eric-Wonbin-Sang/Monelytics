import datetime
import calendar
import dateutil
import glob
import os
import time
from dateutil import relativedelta
from bs4 import BeautifulSoup

from Banks.Generic import Account
from Banks.Venmo import VenmoStatement


class VenmoAccount(Account.Account):

    def __init__(self, parent_bank, driver, source_info_dir, do_download):

        super().__init__(
            parent_bank=parent_bank,
            driver=driver,
            name="Personal Account",
            source_info_dir=source_info_dir,
            base_url="https://venmo.com",
            statement_suffix_url="/account/statement",
            default_statement_csv_name="venmo_statement.csv",
            do_download=do_download
        )

        if self.do_download:
            self.profile_id, self.type = self.get_profile_id_and_type()
            self.base_download_url = self.get_base_download_url()
            self.start_end_date_tuple_list = self.get_start_end_date_tuple_list()
            self.download_and_store()
        else:
            self.profile_id, self.type, self.start_end_date_tuple_list = None, None, []

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
               "&profileId={}".format(self.profile_id if self.do_download else "DNE") + \
               "&accountType={}".format(self.type if self.do_download else "DNE")

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

    def try_to_get_csv_path(self):
        base_time = datetime.datetime.now()
        while (datetime.datetime.now() - base_time).seconds < 2:
            if len(csv_list := glob.glob(self.user_download_dir + "/" + self.default_statement_csv_name)) > 0:
                return csv_list[0]
            print(".", end="")
            time.sleep(.1)
        return None

    def download_and_store(self):
        if self.current_statement_csv_name in os.listdir(self.download_dir):
            os.remove(self.download_dir + "/" + self.current_statement_csv_name)

        for i, (start_date_str, end_date_str) in enumerate(self.start_end_date_tuple_list):
            download_url = self.base_download_url.format(start_date=start_date_str, end_date=end_date_str)
            print(start_date_str, end_date_str, "   ", end="")

            if i == 0:
                new_csv_name = self.current_statement_csv_name
            else:
                new_csv_name = "{} to {}.csv".format(start_date_str, end_date_str)
            new_cvs_path = self.download_dir + "/" + new_csv_name

            if not os.path.exists(new_cvs_path):
                self.driver.get(download_url)
                os.rename(self.try_to_get_csv_path(), new_cvs_path)
                print(new_cvs_path, "created!")
            else:
                print(new_cvs_path, "exists!")

    def get_statement_list(self):
        return [
            VenmoStatement.VenmoStatement(
                parent_account=self,
                file_name=file_name,
                source_directory=self.download_dir
            ) for file_name in os.listdir(self.download_dir)
        ]
