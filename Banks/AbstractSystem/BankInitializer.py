import os
import pickle
import time
from selenium.common import exceptions

from Banks.AbstractSystem import bank_helper

from General import Constants, Functions


def get_driver_cookies_on_close(driver):
    driver_cookies = None
    while True:
        try:
            driver_cookies = driver.get_cookies()
        except exceptions.WebDriverException:
            break
        time.sleep(.2)
    return driver_cookies


def get_bank_file_path_list(bank_type):
    file_path_list = []
    for path in Functions.get_path_list_in_dir(Constants.bank_source_info_dir):
        if bank_type == path.split("/")[-1].split(" - ")[0]:
            file_path_list.append(path)
    return file_path_list


def get_new_bank_dir_path(bank_type):
    num_list = [int(path.split("/")[-1].split(" - ")[1]) for path in get_bank_file_path_list(bank_type)]
    bank_num = 0
    while True:
        if bank_num not in num_list:
            return Constants.bank_source_info_dir + "/" + bank_type + " - {}".format(bank_num)
        bank_num += 1


def bank_setup(bank_type):

    data_dict = {
        "nickname": input("bank's nickname: "),
        "owner": input("owner: "),
        "username": input("username: "),
        "password": input("password: ")
    }

    for path in get_bank_file_path_list(bank_type):
        info_dict = Functions.parse_json(path + "/profile.json")
        if info_dict["username"] == data_dict["username"]:
            print("That username already exists for bank_type {} in the system!".format(bank_type))
            exit()

    driver = bank_helper.get_driver(startup_url=bank_helper.get_bank_info_dict(bank_type)["login_url"])

    driver_cookies = get_driver_cookies_on_close(driver)

    bank_dir_path = get_new_bank_dir_path(bank_type)
    os.mkdir(bank_dir_path)
    pickle.dump(driver_cookies, open(bank_dir_path + "/cookies.pkl", "wb"))
    Functions.dict_to_json(data_dict, bank_dir_path + "/profile.json")
    print("Cookies and profile dict saved at " + bank_dir_path)
