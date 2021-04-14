import os

from PastSystem.Classes.ChildClasses.BofASystem import BofABank
from PastSystem.Classes.ChildClasses.DiscoverSystem import DiscoverBank
from PastSystem.Classes.ChildClasses.VenmoSystem import VenmoBank
from PastSystem.Classes.ChildClasses.ChaseSystem import ChaseBank

from FutureSystem.Classes import Scenario

from General import Functions, Constants


class Profile:

    type_to_bank_class_dict = {
        "Bank of America": BofABank.BofABank,
        "Discover": DiscoverBank.DiscoverBank,
        "Chase": ChaseBank.ChaseBank,
        "Venmo": VenmoBank.VenmoBank,
        # "Mint": Bank.Bank
    }

    def __init__(self, name, source_dir):

        self.name = name
        self.source_dir = source_dir

        self.past_system_dir = self.source_dir + "/past_system"
        self.past_system_graph_path = self.past_system_dir + "/accounts_graph.html"
        self.temp_download_dir = self.past_system_dir + "/temp"
        self.banks_dir = self.past_system_dir + "/banks_dir"
        self.bank_logins_json = self.past_system_dir + "/bank_logins.json"

        self.future_system_dir = self.source_dir + "/future_system"
        self.scenarios_dir = self.future_system_dir + "/scenarios_dir"
        self.future_system_graph_path = self.future_system_dir + "/future_system_graph.html"

        self.bank_list = self.get_full_bank_list()
        self.scenario_list = self.get_scenario_list()

    def get_existing_bank_list(self, banks_dir):
        existing_bank_list = []
        for dir_name in os.listdir(banks_dir):
            if not os.path.isdir(banks_dir + "/" + dir_name):
                continue
            bank_json_path = banks_dir + "/" + dir_name + "/" + "bank.json"
            bank_dict = Functions.parse_json(bank_json_path)
            bank_class = self.type_to_bank_class_dict.get(bank_dict["type"])
            if bank_class:
                existing_bank_list.append(bank_class(self, dir_name=dir_name, **bank_dict))
                print("Found Bank:", existing_bank_list[-1].type, existing_bank_list[-1].username)
            else:
                print("unknown bank type:", bank_dict["type"])
        return existing_bank_list

    def get_bank_list(self, bank_dict_list, existing_bank_list):
        bank_list = []
        for bank_dict in bank_dict_list:
            if bank_dict in [existing_bank.bank_dict for existing_bank in existing_bank_list]:
                continue
            bank_class = self.type_to_bank_class_dict.get(bank_dict["type"])
            if bank_class:
                bank_list.append(bank_class(self, dir_name=None, **bank_dict))
                print("Created Bank:", bank_list[-1].type, bank_list[-1].username)
            else:
                print("unknown bank type:", bank_dict["type"])
        return bank_list

    def get_full_bank_list(self):
        existing_bank_list = self.get_existing_bank_list(self.banks_dir)
        bank_dict_list = Functions.parse_json(self.bank_logins_json)
        new_bank_list = self.get_bank_list(bank_dict_list, existing_bank_list)
        return existing_bank_list + new_bank_list

    def get_scenario_list(self):
        scenario_list = []
        for file_name in os.listdir(self.scenarios_dir):
            file_path = self.scenarios_dir + "/" + file_name
            scenario_list.append(Scenario.Scenario(self, file_path))
        return scenario_list

    def __str__(self):
        return "Profile '{}' -> {}".format(
            self.name,
            self.source_dir
        )


def get_profile_list(monelytics_folder=Constants.monelytics_folder):
    profile_list = []
    for profile_name in os.listdir(monelytics_folder):
        profile_list.append(
            Profile(
                name=profile_name,
                source_dir=monelytics_folder + "/" + profile_name
            )
        )
    return profile_list


if __name__ == '__main__':
    for p in get_profile_list():
        print(p)
