import datetime

from Banks.Generic import Transaction


class VenmoTransaction(Transaction.Transaction):

    def __init__(self, parent_statement, raw_data_dict):

        self.raw_data_dict = raw_data_dict

        super().__init__(
            parent_statement=parent_statement,
            datetime=datetime.datetime.strptime(raw_data_dict["Datetime"], "%Y-%m-%dT%H:%M:%S"),
            amount=self.get_amount(),
            description=self.get_description()
        )

    def get_amount(self):
        is_positive = self.raw_data_dict["Amount (total)"][0] == "+"
        number = float(self.raw_data_dict["Amount (total)"][3:].replace(",", ""))
        return number if is_positive else number * -1

    def get_description(self):
        if self.raw_data_dict["From"] == "" and self.raw_data_dict["To"] == "":
            return "Moved funds to {}".format(self.raw_data_dict["Destination"])
        return "From {} to {}: ".format(self.raw_data_dict["From"], self.raw_data_dict["To"]) \
               + self.raw_data_dict["Note"]
