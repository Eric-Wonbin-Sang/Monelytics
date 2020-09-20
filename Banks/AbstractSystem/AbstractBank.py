from Banks.AbstractSystem import AbstractAccount, AbstractStatement, Transaction

from General import Functions


class AbstractBank:

    def __init__(self, bank_folder_dir, bank_type, statement_class=AbstractStatement.AbstractStatement,
                 transaction_class=Transaction.Transaction):

        self.bank_folder_dir = bank_folder_dir
        self.bank_type = bank_type
        self.statement_class = statement_class
        self.transaction_class = transaction_class

        self.profile_dict = Functions.parse_json(self.bank_folder_dir + "/profile.json")

        self.abstract_account_list = self.get_abstract_account_list()

    def get_account_dir_list(self):
        return [path for path in Functions.get_path_list_in_dir(self.bank_folder_dir)
                if "Account" == path.split("/")[-1].split(" - ")[0]]

    def get_abstract_account_list(self):
        return [
            AbstractAccount.AbstractAccount(parent_bank=self,
                                            account_folder_dir=path,
                                            statement_class=self.statement_class,
                                            transaction_class=self.transaction_class)
            for path in self.get_account_dir_list()
        ]

    def __str__(self):
        ret_str = "Abstract Bank\n\tprofile_dict: {}\n\tbank_folder_dir: {}\n\taccount_list:\n".format(
            self.profile_dict,
            self.bank_folder_dir
        ) + "\t\t------------\n"
        for i, account in enumerate(self.abstract_account_list):
            if i != 0:
                ret_str += "\n"
            ret_str += Functions.tab_str(str(account), 2)
        return ret_str + "\n\t\t------------"
