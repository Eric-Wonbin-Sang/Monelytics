from AccountParsers import Day


class Statement:

    def __init__(self, **kwargs):

        self.transaction_list = kwargs.get("transaction_list")

        self.day_transaction_list_dict = self.get_day_transaction_list_dict()

        self.day_list = self.get_day_list()

        for day in self.day_list:
            print(day)

    def get_day_transaction_list_dict(self):
        day_transaction_list_dict = {}
        for transaction in self.transaction_list:
            if transaction.datetime in day_transaction_list_dict:
                day_transaction_list_dict[transaction.datetime] += [transaction]
            else:
                day_transaction_list_dict[transaction.datetime] = [transaction]
        return day_transaction_list_dict

    def get_day_list(self):
        day_list = []
        for transaction in self.transaction_list:
            appended_bool = False
            for day in day_list:
                if transaction.datetime.date() == day.time_spec:
                    day.add_transaction(transaction)
                    appended_bool = True
                    break
            if not appended_bool:
                day_list.append(Day.Day(time_spec=transaction.datetime.date(),
                                        transaction_list=[transaction]))
        return day_list

    def __str__(self):
        ret_str = ""
        i = 1
        if i == 0:
            for d_i, day in enumerate(self.day_transaction_list_dict):
                if d_i != 0:
                    ret_str += "\n"
                ret_str += "Day: {}".format(day)
                for transaction in self.day_transaction_list_dict[day]:
                    ret_str += "\n\t{}".format(transaction)
            return ret_str
        else:
            for d_i, day in enumerate(self.day_transaction_list_dict):
                if d_i != 0:
                    ret_str += "\n"
                ret_str += "{} Day: {} - transaction count: {}".format(d_i, day, len(self.day_transaction_list_dict[day]))
            return ret_str
