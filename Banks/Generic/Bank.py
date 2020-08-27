import os
import pickle
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from General import Constants


class Bank:

    def __init__(self, profile, login_url, login_cookies_pkl, do_download=False):

        self.profile = profile

        self.name = profile.type
        self.login_url = login_url
        self.chrome_driver_path = Constants.chrome_driver_path
        self.login_cookies_pkl = login_cookies_pkl
        self.do_download = do_download

        self.source_info_dir = self.get_source_info_dir(Constants.bank_source_info_dir)

        if self.do_download:
            self.driver = self.get_driver()
            self.login()
            self.account_list = self.get_account_list()
            self.driver.quit()
        else:
            self.driver = None
            self.account_list = self.get_account_list()

        # self.statement_list = self.get_statement_list()

    def get_source_info_dir(self, parent_dir):
        if not os.path.exists(parent_dir):
            os.mkdir(parent_dir)
        source_info_dir = parent_dir + "/" + self.profile.type + " - " + self.profile.nickname
        if not os.path.exists(source_info_dir):
            os.mkdir(source_info_dir)
        return source_info_dir

    def get_driver(self, detach=True, run_in_background=False):
        options = Options()
        options.add_argument("--app={}".format(self.login_url))
        options.add_argument("window-size={},{}".format(1280, 1000))
        options.add_experimental_option("detach", detach)

        if run_in_background:
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-software-rasterizer')

        driver = webdriver.Chrome(executable_path=self.chrome_driver_path, options=options)

        if os.path.exists(self.login_cookies_pkl):
            for cookie in pickle.load(open(self.login_cookies_pkl, "rb")):
                driver.add_cookie(cookie)
        return driver

    def login(self):
        print(type(self), "does not have an overwritten login function!")
        pass

    def get_account_list(self):
        print(type(self), "does not have an overwritten get_account_list function!")
        return []
