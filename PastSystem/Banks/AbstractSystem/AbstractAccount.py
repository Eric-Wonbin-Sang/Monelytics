import os
import operator

from PastSystem.Banks.AbstractSystem import AbstractStatement

from General import Functions


class AbstractAccount:

    def __init__(self, parent_bank, account_folder_dir, statement_class=AbstractStatement.AbstractStatement):

        self.parent_bank = parent_bank
        self.account_folder_dir = account_folder_dir
        self.statement_class = statement_class

        self.info_dict = self.get_info_dict()

        self.abstract_statement_list = self.get_abstract_statement_list()

        self.full_transaction_list = self.get_full_transaction_list()

    def get_info_dict(self):
        if os.path.exists(profile_json_path := self.account_folder_dir + "/info.json"):
            return Functions.parse_json(profile_json_path)
        return {}

    def get_statement_path_list(self):
        return [
            path for path in Functions.get_path_list_in_dir(self.account_folder_dir)
            if "info.json" != path.split("/")[-1]
        ]

    def get_abstract_statement_list(self):
        return [
            self.statement_class(parent_account=self, statement_file_path=path)
            for path in self.get_statement_path_list()
        ]

    def get_full_transaction_list(self):
        transaction_list = []
        for statement in self.abstract_statement_list:
            transaction_list += statement.transaction_list
        return sorted(transaction_list, key=operator.attrgetter("datetime"), reverse=False)

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
