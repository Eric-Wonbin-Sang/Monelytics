import datetime
import pandas as pd
import matplotlib.pyplot as plt

from FutureSystem.Classes import Projection


def get_complete_df(projection_list):

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
        Projection.Projection(
            name="daily test",
            type="expense",
            start_datetime=datetime.datetime(year=2020, month=10, day=1),
            frequency="daily",
            end_datetime=datetime.datetime(year=2021, month=10, day=14),
            amount=10
        ),
        Projection.Projection(
            name="weekly test",
            type="expense",
            start_datetime=datetime.datetime(year=2020, month=10, day=1),
            frequency="weekly",
            end_datetime=datetime.datetime(year=2021, month=10, day=14),
            amount=30
        ),
        Projection.Projection(
            name="monthly test",
            type="income",
            start_datetime=datetime.datetime(year=2020, month=10, day=1),
            frequency="monthly",
            end_datetime=datetime.datetime(year=2021, month=10, day=14),
            amount=1000
        ),
        Projection.Projection(
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
