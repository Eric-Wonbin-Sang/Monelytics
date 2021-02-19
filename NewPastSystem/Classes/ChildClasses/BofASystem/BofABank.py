import os
import time
import pickle
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from NewPastSystem.Classes.ParentClasses import Bank
from NewPastSystem.Classes.ChildClasses.BofASystem import BofAParser


class BofABank(Bank.Bank):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.login_url = "https://www.bankofamerica.com/"
        self.auth_url = "https://secure.bankofamerica.com/login/sign-in/entry/signOnV2.go"
        # self.cookies_path = self.general_path + "/cookies.pkl"    # doesn't need it after you remember the comp

        self.get_statements()

    def get_statements(self):
        bofa_parser = BofAParser.BofAParser(bofa_bank=self, cookies_path=None)

    def __str__(self):
        return "BofA Bank - type: {}, id: {}\n\towner: {}\n\tusername: {}\n\tpassword: {}".format(
            self.type,
            self.id,
            self.owner,
            self.username,
            "*" * len(self.password)
        )
