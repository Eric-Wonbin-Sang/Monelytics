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

        self.amount = kwargs.get("amount") if self.type == "income" else kwargs.get("amount") * -1

        self.datetime_amount_df = self.get_datetime_amount_df()

    def get_datetime_amount_df(self):
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

        data = {
            "date": datetime_list,
            "amount": amount_list
        }
        return pd.DataFrame(data, columns=list(data.keys()))

    def plot(self):
        plt.plot(
            'date', 'amount',
            data=self.datetime_amount_df,
            marker='.',
            color=(0, 0, 1),
            linewidth=1,
            linestyle='--',
            label="{} ({})".format(self.name, self.type)
        )

    def __str__(self):
        return "Projection: {}, {}".format(
            self.name,
            self.type
        )
