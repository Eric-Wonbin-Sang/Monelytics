from PastSystem.Banks.AbstractSystem import bank_helper, AbstractBank


class UpdateBot:

    def __init__(self, bank_folder_dir, bank_type):

        self.bank_folder_dir = bank_folder_dir
        self.bank = AbstractBank.AbstractBank(bank_folder_dir=self.bank_folder_dir)

        self.cookies_path = self.bank_folder_dir + "/cookies.pkl"
        self.login_url = bank_helper.get_bank_info_dict(bank_type)["login_url"]

        self.driver = self.get_driver()

        self.login()
        self.download_statements()

        self.driver.close()

    def get_driver(self, detach=True, run_in_background=False):
        return bank_helper.get_driver(
            startup_url=self.login_url,
            cookies_path=self.cookies_path,
            detach=detach,
            run_in_background=run_in_background
        )

    def login(self):
        pass

    def download_statements(self):
        pass
