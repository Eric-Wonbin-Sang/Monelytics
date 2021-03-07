import datetime
import pandas as pd
import matplotlib.pyplot as plt

from FutureSystem.Classes import Projection
from FutureSystem.Classes.CustomClasses import SalaryIncome

from General import Functions

pd.set_option('display.expand_frame_repr', False)


def get_complete_df(projection_list):

    # datetime_list = pd.date_range(
    #     start=datetime.datetime(year=2020, month=10, day=14),
    #     periods=365 * 6
    # ).to_pydatetime().tolist()

    dataframe_list = []
    for projection in projection_list:
        dataframe_list.append(
            projection.dataframe.rename(columns={"result": "{} result".format(projection.name)})
        )
    complete_df = pd.concat(dataframe_list)
    complete_df = complete_df.sort_index()

    copy_df = complete_df.where(pd.notnull(complete_df), 0)
    copy_df["result"] = copy_df.sum(axis=1)

    delta_list = []
    for value in copy_df["result"]:
        if not delta_list:
            delta_list.append(value)
        else:
            delta_list.append(value + delta_list[-1])
    complete_df["result"] = delta_list
    return complete_df


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
        ),
        SalaryIncome.SalaryIncome(
            name="example income",
            yearly_income=60000,
            income_frequency="monthly",
            income_tax=.24,
            income_start=datetime.datetime(year=2021, month=8, day=1),
            income_end=datetime.datetime(year=2025, month=8, day=1),
            bonus=2000,
            bonus_frequency="yearly",
            bonus_tax=.30,
            bonus_start=datetime.datetime(year=2021, month=8, day=1),
            bonus_end=datetime.datetime(year=2025, month=8, day=1)
        )
    ]

    complete_df = get_complete_df(projection_list)

    for p in projection_list:
        plt.plot(
            p.dataframe.index,
            p.dataframe["result"],
            alpha=0.8,
            marker=".",
            label=p.name
        )

    plt.plot(
        complete_df.index,
        complete_df["result"],
        alpha=0.8,
        marker=".",
        label="running total"
    )
    plt.legend(loc='upper left')

    plt.grid()
    plt.show()


if __name__ == '__main__':
    main()
