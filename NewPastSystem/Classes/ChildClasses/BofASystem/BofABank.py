import os
import time
import pickle
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from NewPastSystem.Classes.ParentClasses import Bank


class BofABank(Bank.Bank):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.login_url = "https://www.bankofamerica.com/"
        self.auth_url = "https://secure.bankofamerica.com/login/sign-in/entry/signOnV2.go"
        # self.cookies_path = self.general_path + "/cookies.pkl"    # doesn't need it after you remember the comp

        self.get_statements()

    def get_statements(self):

        options = Options()
        options.add_argument("window-size={},{}".format(1280, 1000))
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        # if os.path.exists(self.cookies_path):
        #     for cookie in pickle.load(open(self.cookies_path, "rb")):
        #         print(cookie)
        #         driver.add_cookie(cookie)
        driver.get(self.login_url)

        # logging in
        driver.find_element_by_name("onlineId1").send_keys(self.username)
        time.sleep(1)
        driver.find_element_by_name("passcode1").send_keys(self.password)
        driver.find_element_by_id("signIn").send_keys(Keys.RETURN)
        time.sleep(2)

        # set up two factor authentication (only requires it once)
        while driver.current_url == self.auth_url:

            send_code_button = driver.find_element_by_id("btnARContinue")
            send_code_button.send_keys(Keys.RETURN)

            auth_code = input("Please input two factor auth code: ")

            auth_code_box = driver.find_element_by_id("tlpvt-acw-authnum")
            auth_code_box.clear()
            auth_code_box.send_keys(auth_code)

            recognize_computer_radio = driver.find_element_by_id("yes-recognize")
            recognize_computer_radio.click()

            submit_button = driver.find_element_by_id("continue-auth-number")
            submit_button.send_keys(Keys.RETURN)

        # if os.path.exists(self.cookies_path):
        #     os.remove(self.cookies_path)
        # pickle.dump(driver.get_cookies(), open(self.cookies_path, "wb"))

        # getting accounts
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        account_elem_list = soup.findAll("div", {"class": "AccountItem"})
        for i, account_elem in enumerate(account_elem_list):
            account_name_elem = account_elem.findAll("span", {"class": "AccountName"})[0]
            list_elem = account_name_elem.findAll("a")[0]
            print(list_elem)
            info_dict = {
                "name": list_elem.text,
                "account_type": account_elem.get("data-accounttype"),
                "account_url": "https://secure.bankofamerica.com" + list_elem.get("href")
            }
            for key, value in info_dict.items():
                print("\t", key, value)
            print("---")
            #
            # if account := self.try_get_account(info_dict):
            #     account_folder_dir = account.account_folder_dir
            # else:
            #     account_folder_dir = self.get_new_account_folder_dir()
            #     os.mkdir(account_folder_dir)
            #     Functions.dict_to_json(info_dict, account_folder_dir + "/info.json")

        input("test")

    def __str__(self):
        return "BofA Bank - type: {}, id: {}\n\towner: {}\n\tusername: {}\n\tpassword: {}".format(
            self.type,
            self.id,
            self.owner,
            self.username,
            "*" * len(self.password)
        )
