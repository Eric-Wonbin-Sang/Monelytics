import os

from Banks.AbstractSystem import AbstractStatement

from General import Functions


class AbstractAccount:

    def __init__(self, parent_bank, account_folder_dir):

        self.parent_bank = parent_bank
        self.account_folder_dir = account_folder_dir
        self.info_dict = self.get_info_dict()

        self.abstract_statement_list = self.get_abstract_statement_list()

    def get_info_dict(self):
        if os.path.exists(profile_json_path := self.account_folder_dir + "/info.json"):
            return Functions.parse_json(profile_json_path)
        return {}

    def get_abstract_statement_list(self):
        return [
            AbstractStatement.AbstractStatement(parent_account=self, statement_file_path=path)
            for path in Functions.get_path_list_in_dir(self.account_folder_dir)
        ]

    def __str__(self):
        ret_str = "Abstract Account\n\tinfo_dict: {}\n\taccount_folder_dir: {}\n\taccount_list:\n".format(
            self.info_dict,
            self.account_folder_dir
        )
        for i, statement in enumerate(self.abstract_statement_list):
            if i != 0:
                ret_str += "\n"
            ret_str += Functions.tab_str(str(statement), 3)
        return ret_str
