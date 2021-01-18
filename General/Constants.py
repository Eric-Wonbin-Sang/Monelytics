import os
from General import Functions


bank_source_info_dir = Functions.get_curr_parent_dir("/0 - Secrets/Monelytics/Bank Source Information")

current_statement_file_name_default = "Current transactions.csv"    # move to to-be-created account parent class

user_download_dir = "C:/Users/ericw/Downloads"

project_dir = "/".join(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/").split("/")[:-1])
projects_dir = "/".join(project_dir.split("/")[:-1])
secrets_dir = projects_dir + "/" + "0 - Secrets"
