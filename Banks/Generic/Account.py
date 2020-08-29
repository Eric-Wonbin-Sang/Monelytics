import os
import datetime

from General import Constants


class Account:

    def __init__(self, parent_bank, **kwargs):

        self.curr_datetime = datetime.datetime.now()

        self.parent_bank = parent_bank
        self.driver = kwargs["driver"]
        self.name = kwargs["name"]
        self.source_info_dir = kwargs["source_info_dir"]
        self.base_url = kwargs["base_url"]
        self.statement_suffix_url = kwargs["statement_suffix_url"]
        self.statement_url = self.get_statement_url()

        self.user_download_dir = Constants.user_download_dir
        self.download_dir = self.get_download_dir()

        self.default_statement_csv_name = kwargs["default_statement_csv_name"]
        self.current_statement_csv_name = Constants.current_statement_file_name_default

        self.do_download = kwargs["do_download"]

        self.statement_list = self.get_statement_list()

    def get_statement_url(self):
        return self.base_url + self.statement_suffix_url if self.base_url and self.statement_suffix_url else None

    def get_download_dir(self):
        download_dir = self.source_info_dir + "/" + self.name
        if not os.path.exists(download_dir):
            os.mkdir(download_dir)
        return download_dir

    def download_and_store(self):
        print(type(self), "does not have an overwritten download_and_store function!")
        pass

    def get_statement_list(self):
        print(type(self), "does not have an overwritten get_statement_list function!")
        return []

    def __str__(self):
        return "{} Acct | name: {}  source_info_dir: {}".format(
            self.parent_bank.name,
            self.name,
            self.source_info_dir
        )
