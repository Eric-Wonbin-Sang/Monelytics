
from General import Functions


class Statement:

    def __init__(self, **kwargs):

        self.parent_account = kwargs["parent_account"]

        self.file_name = kwargs["file_name"]
        self.source_directory = kwargs["source_directory"]
        self.file_path = self.source_directory + "/" + self.file_name

        self.data_list_list = Functions.csv_to_list_list(self.file_path)

        self.info_dict, self.dataframe, self.transaction_list = {}, None, []

    def get_transaction_list(self):
        print(type(self), "does not have an overwritten get_transaction_list function!")
        return []
