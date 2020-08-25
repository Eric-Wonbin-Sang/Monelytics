import os
from General import Functions


chrome_driver_path = Functions.get_curr_parent_dir("/API Keys/chromedriver.exe")

profile_list_json = Functions.get_curr_parent_dir("/0 - Secrets/Monelytics/profile_list.json")

bofa_login_cookies_pkl = Functions.get_curr_parent_dir("/API Keys/Monelytics/bofa - login cookies.pkl")
bofa_accounts_download_dir = Functions.get_curr_parent_dir("/0 - Secrets/Monelytics/Bank of America")

user_download_dir = "C:/Users/ericw/Downloads"

project_dir = "/".join(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/").split("/")[:-1])
