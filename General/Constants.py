import os
from General import Functions


# unsorted or old ----------------------------------------------

bank_source_info_dir = Functions.get_curr_parent_dir() + "/0 - Secrets/Monelytics/Bank Source Information"
current_statement_file_name_default = "Current transactions.csv"    # move to to-be-created account parent class
user_download_dir = "C:/Users/ericw/Downloads"

# projects dirs ----------------------------------------------

project_dir = "/".join(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/").split("/")[:-1])
projects_dir = "/".join(project_dir.split("/")[:-1])
secrets_dir = projects_dir + "/" + "0 - Secrets"
do_download = False

# project dirs and paths -------------------------------------

# monelytics_folder = secrets_dir + "/Monelytics"
monelytics_folder = "C:/Users/ericw/Desktop/Monelytics"

past_system_dir = monelytics_folder + "/past_system"
past_system_graph_path = past_system_dir + "/accounts_graph.html"
temp_download_dir = past_system_dir + "/temp"
banks_dir = past_system_dir + "/banks_dir"
bank_logins_json = past_system_dir + "/bank_logins.json"

future_system_dir = monelytics_folder + "/future_system"
projections_dir = future_system_dir + "/projections_dir"
