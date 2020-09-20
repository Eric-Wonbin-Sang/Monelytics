import pickle
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from Banks.AbstractSystem import AbstractBank

from General import Functions, Constants


class UpdateBot:

    def __init__(self, bank_folder_dir, bank_type):

        self.bank_folder_dir = bank_folder_dir
        self.bank = AbstractBank.AbstractBank(bank_folder_dir=self.bank_folder_dir)

        self.cookies_path = self.bank_folder_dir + "/cookies.pkl"
        self.login_url = Functions.parse_json(Constants.project_dir + "/Banks/bank_constants.json")[bank_type]

        self.driver = self.get_driver()

        self.login()
        self.download_statements()

        self.driver.close()

    def get_driver(self, detach=True, run_in_background=False):
        options = Options()
        options.add_argument("--app={}".format(self.login_url))
        options.add_argument("window-size={},{}".format(1280, 1000))
        options.add_experimental_option("detach", detach)

        if run_in_background:
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-software-rasterizer')

        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        if os.path.exists(self.cookies_path):
            for cookie in pickle.load(open(self.cookies_path, "rb")):
                driver.add_cookie(cookie)
        return driver

    def login(self):
        pass

    def download_statements(self):
        pass
