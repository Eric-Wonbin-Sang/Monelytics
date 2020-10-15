import os
import pickle
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from General import Functions, Constants


def get_driver(startup_url=None, cookies_path=None, detach=True, run_in_background=False):
    options = Options()

    if startup_url:
        options.add_argument("--app={}".format(startup_url))

    options.add_argument("window-size={},{}".format(1280, 1000))
    options.add_experimental_option("detach", detach)

    if run_in_background:
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-software-rasterizer')

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    if cookies_path and os.path.exists(cookies_path):
        for cookie in pickle.load(open(cookies_path, "rb")):
            driver.add_cookie(cookie)
    return driver


def get_bank_info_dict(bank_type):
    for data_dict in Functions.parse_json(Constants.project_dir + "/Banks/bank_info.json"):
        if data_dict["type"] == bank_type:
            return data_dict
    raise UserWarning("Bank type DNE in bank_info.json - {}".format(bank_type))
