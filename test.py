import datetime
import calendar
import pandas as pd
import matplotlib.pyplot as plt


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
                curr_datetime = add_months(curr_datetime, 1)
            elif self.frequency == "yearly":
                curr_datetime = add_months(curr_datetime, 12)

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


def add_months(source_date, months):
    month = source_date.month - 1 + months
    year = source_date.year + month // 12
    month = month % 12 + 1
    day = min(source_date.day, calendar.monthrange(year, month)[1])
    return datetime.datetime(year, month, day)


def get_complete_df(projection_list):
    # complete_df = pd.concat(projection_list)

    datetime_list = pd.date_range(
        start=datetime.datetime(year=2020, month=10, day=14),
        periods=365 * 4
    ).to_pydatetime().tolist()
    delta_list_list = []
    for projection in projection_list:
        delta_list = []
        for i, some_datetime in enumerate(datetime_list):
            search_df = projection.datetime_amount_df.loc[projection.datetime_amount_df['date'] == some_datetime]

            value = search_df["amount"].iloc[0] if not search_df.empty else 0

            if i == 0:
                delta_list.append(value)
            else:
                delta_list.append(delta_list[-1] + value)
        delta_list_list.append(delta_list)

    delta_list = [sum(i) for i in zip(*delta_list_list)]

    data = {
        "date": datetime_list,
        "delta": delta_list
    }
    return pd.DataFrame(data, columns=list(data.keys()))


def main():

    projection_list = [
        Projection(
            name="daily test",
            type="expense",
            start_datetime=datetime.datetime(year=2020, month=10, day=1),
            frequency="daily",
            end_datetime=datetime.datetime(year=2021, month=10, day=14),
            amount=10
        ),
        Projection(
            name="weekly test",
            type="expense",
            start_datetime=datetime.datetime(year=2020, month=10, day=1),
            frequency="weekly",
            end_datetime=datetime.datetime(year=2021, month=10, day=14),
            amount=30
        ),
        Projection(
            name="monthly test",
            type="income",
            start_datetime=datetime.datetime(year=2020, month=10, day=1),
            frequency="monthly",
            end_datetime=datetime.datetime(year=2021, month=10, day=14),
            amount=1000
        ),
        Projection(
            name="yearly test",
            type="income",
            start_datetime=datetime.datetime(year=2020, month=10, day=1),
            frequency="yearly",
            end_datetime=datetime.datetime(year=2021, month=10, day=14),
            amount=50
        )
    ]
    for projection in projection_list:
        projection.plot()

    complete_df = get_complete_df(projection_list)

    ax = plt.gca()
    complete_df.plot(kind='line', x='date', y='delta', color='red', ax=ax)

    plt.grid()
    plt.show()


if __name__ == '__main__':
    main()
