import os

from General import Constants


class Bank:

    banks_dir = Constants.banks_dir

    def __init__(self, **kwargs):

        self.type = kwargs.get("bank_type")
        self.id = kwargs.get("bank_id")
        self.owner = kwargs.get("owner")
        self.username = kwargs.get("username")
        self.password = kwargs.get("password")

        self.dir_name = self.generate_dir_name()

        if not os.path.isdir(self.banks_dir + "/" + self.dir_name):
            self.setup_directories()

    def generate_dir_name(self):
        return "{}_{}".format(
            self.type,
            self.id
        )

    def setup_directories(self):
        bank_path = self.banks_dir + "/" + self.dir_name
        os.mkdir(bank_path)
        os.mkdir(bank_path + "/" + "source_files")

    def __str__(self):
        return "Generic Bank - type: {}, id: {}\n\towner: {}\n\tusername: {}\n\tpassword: {}".format(
            self.type,
            self.id,
            self.owner,
            self.username,
            "*" * len(self.password)
        )
