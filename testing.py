from selenium.webdriver import Chrome
import dateutil.relativedelta
import selenium.webdriver
import os
from selenium.webdriver.common.keys import Keys
# import cPickle as pickle

import pickle
# import SendKeys
import time
import datetime
import os

CHROME_DRIVER_PATH = "chromedriver.exe"
VENMO_URL = 'https://venmo.com/'

venmo_email = input("Venmo email: ")
venmo_password = input("Venmo password: ")
download_folder = os.path.dirname(os.path.abspath(__file__)) + "\\Data Download"

chromeOptions = selenium.webdriver.ChromeOptions()
chromeOptions.add_experimental_option("prefs", {"download.default_directory": download_folder})
global_browser = selenium.webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, chrome_options=chromeOptions)

print("hello")

# global_browser = Chrome(CHROME_DRIVER_PATH)


def find_elem(parent, method, search_key):
    elem = None
    if method == "name":
        elem = parent.find_element_by_name(search_key)
    elif method == "class_name":
        elem = parent.find_element_by_class_name(search_key)
    elif method == "tag_name":
        elem = parent.find_element_by_tag_name(search_key)
    return elem


def enter_login_credentials(browser):
    find_elem(parent=browser, method="class_name", search_key="sign-in").click()
    find_elem(parent=browser, method="name", search_key="phoneEmailUsername").send_keys(venmo_email)
    find_elem(parent=browser, method="name", search_key="password").send_keys(venmo_password)
    find_elem(parent=find_elem(parent=browser, method="class_name", search_key="button-wrapper"),
              method="class_name", search_key="ladda-label").click()


def add_cookies_to_browser(browser, cookie_file):
    for cookie in pickle.load(open(cookie_file, "rb")):
        if 'expiry' in cookie:
            del cookie['expiry']
        browser.add_cookie(cookie)


def first_login(browser):
    enter_login_credentials(browser)
    time.sleep(1)
    find_elem(parent=browser, method="class_name", search_key="ladda-label").click()

    verification_code = input("Enter Verification Code: ")

    find_elem(parent=browser, method="class_name", search_key="auth-form-input")\
        .send_keys(verification_code)
    find_elem(parent=browser, method="class_name", search_key="ladda-label").click()
    time.sleep(1)
    find_elem(parent=browser, method="class_name", search_key="ladda-label").click()
    pickle.dump(browser.get_cookies(), open("cookies.pkl", "wb"))


def subtract_months(date, months_to_subtract):
    return date - dateutil.relativedelta.relativedelta(months=months_to_subtract)


def download_transaction_history(browser):
    now = datetime.datetime.now()
    end = "end={}".format(now.strftime("%m-%d-%Y"))
    start = "start={}".format(subtract_months(now, 1).strftime("%m-%d-%Y"))
    browser.get("https://venmo.com/account/statement?{}&{}".format(end, start))
    find_elem(parent=find_elem(parent=browser, method="class_name", search_key="statement-buttons"),
              method="tag_name", search_key="button").click()

    while True:
        file_list = os.listdir(download_folder)
        if file_list:
            file_path = file_list[0]
            break
        time.sleep(1)
    return file_path


# def parse_transaction_history():




def main():

    browser = global_browser
    browser.get(VENMO_URL)

    if not os.path.isfile('cookies.pkl'):
        first_login(browser)
    else:
        add_cookies_to_browser(browser, cookie_file="cookies.pkl")
        enter_login_credentials(browser)

    time.sleep(2)

    transaction_history_path = download_transaction_history(browser)
    print(transaction_history_path)

    time.sleep(10)


main()
# time.sleep(60)

# Save the cookies
# pickle.dump(browser.get_cookies(), open("cookies.pkl", "wb"))

# if os.path.isfile('cookies.pkl'):
#     # there is a cookie file
#
#     cookies = pickle.load(open("cookies.pkl", "rb"))
#     for cookie in cookies:
#         browser.add_cookie(cookie)
#
#     # click on the sign in link
#     signin_link = browser.find_element_by_link_text("Sign in")
#     signin_link.click()
#
#     # enter the email and password and send it
#     username_box = browser.find_element_by_class_name("email-username-phone")
#     username_box.send_keys(venmoInfo.my_u)
#     password_box = browser.find_element_by_class_name("password")
#     password_box.send_keys(venmoInfo.my_p)
#     send_button = browser.find_element_by_class_name("login")
#     send_button.click()
#
#     # # enter the person's name you want to pay
#     # time.sleep(5)
#     # name_box = browser.find_element_by_class_name("onebox_prefill")
#     # name_box.click()
#     # name_text_box = browser.find_element_by_class_name("paddingUnifier")
#     # name_text_box.send_keys(venmoInfo.payee_name)
#     # name_text_box.send_keys(Keys.ENTER)
#     # payment_box = browser.find_element_by_class_name("mainTextBox")
#     # time.sleep(1)
#     # payment_box.click()
#     # datetime_now = datetime.datetime.now()
#     # SendKeys.SendKeys(venmoInfo.amount + venmoInfo.description, with_spaces=True)
#     # # click the pay button
#     # pay_button = browser.find_element_by_id("onebox_pay_toggle")
#     # pay_button.click()
#     # name_text_box = browser.find_element_by_class_name("paddingUnifier")
#     # name_text_box.send_keys(venmoInfo.payee_name)
#     #
#     # # click the send button
#     # send_button = browser.find_element_by_id("onebox_send_button")
#     # send_button.click()
#
# else:
#     # click on the sign in link
#     signin_link = browser.find_element_by_link_text("Sign in")
#     signin_link.click()
#     print("Couldn't find the cookie file, you will need two factor authorization and then cookie will be saved")
#     # wait a while until the user fully signs in
#     time.sleep(60)
#     # Save the cookies
#     # pickle.dump(browser.get_cookies(), open("cookies.pkl", "wb"))

# time.sleep(10)
# browser.close()