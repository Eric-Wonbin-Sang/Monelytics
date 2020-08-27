import os
from General import Functions


chrome_driver_path = Functions.get_curr_parent_dir("/API Keys/chromedriver.exe")

profile_list_json = Functions.get_curr_parent_dir("/0 - Secrets/Monelytics/profile_list.json")

bank_source_info_dir = Functions.get_curr_parent_dir("/0 - Secrets/Monelytics/Bank Source Information")
bofa_login_cookies_pkl = Functions.get_curr_parent_dir("/0 - Secrets/Monelytics/login cookies - bofa.pkl")
venmo_login_cookies_pkl = Functions.get_curr_parent_dir("/0 - Secrets/Monelytics/login cookies - venmo.pkl")

do_download = False

user_download_dir = "C:/Users/ericw/Downloads"

project_dir = "/".join(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/").split("/")[:-1])
