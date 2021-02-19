import os
import time
import pickle
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class BofAParser:

    login_url = "https://www.bankofamerica.com/"
    auth_url = "https://secure.bankofamerica.com/login/sign-in/entry/signOnV2.go"

    def __init__(self, username, password, cookies_path):

        self.username = username
        self.password = password
        self.cookies_path = cookies_path    # doesn't need it after you remember the comp

        self.driver = self.get_driver()
        self.login()
        self.account_dict_list = self.get_account_dict_list()

    def get_driver(self):
        options = Options()
        options.add_argument("window-size={},{}".format(1280, 1000))
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        if self.cookies_path and os.path.exists(self.cookies_path):
            for cookie in pickle.load(open(self.cookies_path, "rb")):
                driver.add_cookie(cookie)
        return driver

    def login(self):
        self.driver.get(self.login_url)
        self.driver.find_element_by_name("onlineId1").send_keys(self.username)
        time.sleep(1)
        self.driver.find_element_by_name("passcode1").send_keys(self.password)
        self.driver.find_element_by_id("signIn").send_keys(Keys.RETURN)
        time.sleep(2)

        # set up two factor authentication (only requires it once)
        while self.driver.current_url == self.auth_url:
            send_code_button = self.driver.find_element_by_id("btnARContinue")
            send_code_button.send_keys(Keys.RETURN)

            auth_code = input("Please input two factor auth code: ")

            auth_code_box = self.driver.find_element_by_id("tlpvt-acw-authnum")
            auth_code_box.clear()
            auth_code_box.send_keys(auth_code)

            recognize_computer_radio = self.driver.find_element_by_id("yes-recognize")
            recognize_computer_radio.click()

            submit_button = self.driver.find_element_by_id("continue-auth-number")
            submit_button.send_keys(Keys.RETURN)

        # if os.path.exists(self.cookies_path):
        #     os.remove(self.cookies_path)
        # pickle.dump(driver.get_cookies(), open(self.cookies_path, "wb"))

    def get_account_dict_list(self):
        account_dict_list = []
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        account_elem_list = soup.findAll("div", {"class": "AccountItem"})
        for i, account_elem in enumerate(account_elem_list):
            account_name_elem = account_elem.findAll("span", {"class": "AccountName"})[0]
            list_elem = account_name_elem.findAll("a")[0]
            account_dict_list.append(
                {
                    "name": list_elem.text,
                    "account_type": account_elem.get("data-accounttype"),
                    "account_url": "https://secure.bankofamerica.com" + list_elem.get("href")
                }
            )
        return account_dict_list

    def get_account_list(self):
        pass