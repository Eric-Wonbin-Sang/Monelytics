import os
import pickle
import time
from selenium.common import exceptions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from General import Constants


def cookie_getter(save_dir=Constants.user_download_dir):

    options = Options()
    options.add_argument("window-size={},{}".format(1280, 1000))

    driver = webdriver.Chrome(executable_path=Constants.chrome_driver_path, options=options)
    driver.get("https://www.google.com/")

    cookie_path = None
    while True:
        try:
            _ = driver.window_handles
            if os.path.exists((cookie_path := save_dir + "/cookies.pkl")):
                os.remove(cookie_path)
            pickle.dump(driver.get_cookies(), open(cookie_path, "wb"))
        except exceptions.WebDriverException:
            break
        time.sleep(.5)

    print("Cookies saved at {}".format(cookie_path))


cookie_getter()
