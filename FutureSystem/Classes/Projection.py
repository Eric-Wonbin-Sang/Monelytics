import datetime
import pandas as pd

from General import Functions


class Projection:

    def __init__(self, **kwargs):

        self.name = kwargs.get("name")

        self.start_datetime = kwargs.get("start_datetime")
        self.frequency = kwargs.get("frequency")
        self.end_datetime = kwargs.get("end_datetime")

        self.amount = kwargs.get("amount")

        self.dataframe = self.get_dataframe()

    def get_dataframe(self):
        curr_datetime = self.start_datetime
        datetime_list = []
        amount_list = []
        while True:
            if curr_datetime >= self.end_datetime:
                break
            datetime_list.append(curr_datetime)
            amount_list.append(self.amount)

            if self.frequency == "daily":
                curr_datetime += datetime.timedelta(days=1)
            elif self.frequency == "weekly":
                curr_datetime += datetime.timedelta(days=7)
            elif self.frequency == "biweekly":
                curr_datetime += datetime.timedelta(days=14)
            elif self.frequency == "monthly":
                curr_datetime = Functions.add_months(curr_datetime, 1)
            elif self.frequency == "yearly":
                curr_datetime = Functions.add_months(curr_datetime, 12)

        data = {"result": amount_list}
        full_dataframe = pd.DataFrame(data, index=datetime_list, columns=list(data.keys()))
        full_dataframe = full_dataframe.sort_index()
        return full_dataframe

    def to_dict(self):
        return {
            "name": self.name,
            "start_datetime": self.start_datetime.strftime("%Y-%m-%d"),
            "end_datetime": self.end_datetime.strftime("%Y-%m-%d"),
            "frequency": self.frequency,
            "amount": self.amount,
        }

    def __str__(self):
        return "Projection: {}".format(
            self.name
        ) \
               + "\n\tstart_datetime: {}".format(self.start_datetime) \
               + "\n\tend_datetime: {}".format(self.end_datetime) \
               + "\n\tfrequency: {}".format(self.frequency) \
               + "\n\tamount: {}".format(self.amount)


def combine_projection_dfs(dataframe_0, dataframe_1, amount_type):
    """ This assumes the date ranges for each dataframes are the same. """
    data = {
        "prev_result_0": dataframe_0["result"],
        "prev_result_1": dataframe_1["result"]
    }
    full_dataframe = pd.DataFrame(data, index=dataframe_0.index, columns=list(data.keys()))
    full_dataframe = full_dataframe.where(pd.notnull(full_dataframe), 0)
    if amount_type == "value":
        full_dataframe["result"] = full_dataframe["prev_result_0"] + full_dataframe["prev_result_1"]
    else:
        full_dataframe["result"] = full_dataframe["prev_result_0"] * full_dataframe["prev_result_1"]
    return full_dataframe


def json_dict_to_projection(json_dict):
    json_dict["start_datetime"] = datetime.datetime.strptime(json_dict["start_datetime"], "%Y-%m-%d")
    json_dict["end_datetime"] = datetime.datetime.strptime(json_dict["end_datetime"], "%Y-%m-%d")
    return Projection(**json_dict)
