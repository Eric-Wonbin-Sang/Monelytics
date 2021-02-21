from NewPastSystem.Classes.ParentClasses import Bank
from NewPastSystem.Classes.ChildClasses.BofASystem import BofAParser


class BofABank(Bank.Bank):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.login_url = "https://www.bankofamerica.com/"
        self.auth_url = "https://secure.bankofamerica.com/login/sign-in/entry/signOnV2.go"
        # self.cookies_path = self.general_path + "/cookies.pkl"    # doesn't need it after you remember the comp

        self.update_accounts()

    def update_accounts(self):
        bofa_parser = BofAParser.BofAParser(bofa_bank=self, cookies_path=None)
        bofa_parser.update_statements()

    # def __str__(self):
    #     return "BofA Bank - type: {}\n\towner: {}\n\tusername: {}\n\tpassword: {}".format(
    #         self.type,
    #         self.owner,
    #         self.username,
    #         "*" * len(self.password)
    #     )
