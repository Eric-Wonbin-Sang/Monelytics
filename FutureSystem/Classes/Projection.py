import datetime
import pandas as pd
import matplotlib.pyplot as plt

from General import Functions


class Projection:

    def __init__(self, **kwargs):

        self.name = kwargs.get("name")
        self.type = kwargs.get("type")

        self.start_datetime = kwargs.get("start_datetime")
        self.frequency = kwargs.get("frequency")
        self.end_datetime = kwargs.get("end_datetime")

        self.amount = kwargs.get("amount")
        self.update_amount()

        self.dataframe = self.get_dataframe()

    def update_amount(self):
        if self.type == "income":
            pass
        else:
            self.amount *= -1
        pass

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
            elif self.frequency == "monthly":
                curr_datetime = Functions.add_months(curr_datetime, 1)
            elif self.frequency == "yearly":
                curr_datetime = Functions.add_months(curr_datetime, 12)

        data = {"result": amount_list}
        full_dataframe = pd.DataFrame(data, index=datetime_list, columns=list(data.keys()))
        full_dataframe = full_dataframe.sort_index()
        return full_dataframe

    def plot(self):
        plt.plot(
            self.dataframe.index,
            self.dataframe["result"],
            alpha=0.8,
            marker="."
        )

    def __str__(self):
        return "Projection: {}, {}".format(
            self.name,
            self.type
        )


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
