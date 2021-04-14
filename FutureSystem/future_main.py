import os
import datetime
import pandas as pd

from FutureSystem.Classes import Projection, Scenario
from FutureSystem.Classes.ComplexProjections import SalaryIncome

from General import Functions, Constants

pd.set_option('display.expand_frame_repr', False)


# def get_scenario_list():
#     scenario_list = []
#     for file_name in os.listdir(Constants.scenarios_dir):
#         file_path = Constants.scenarios_dir + "/" + file_name
#         scenario_list.append(Scenario.Scenario(file_path))
#     return scenario_list


def main():

    projection_list = [
        Projection.Projection(
            name="daily test",
            start_datetime=datetime.datetime(year=2020, month=10, day=1),
            frequency="daily",
            end_datetime=datetime.datetime(year=2021, month=10, day=14),
            amount=10
        ),
        Projection.Projection(
            name="weekly test",
            start_datetime=datetime.datetime(year=2020, month=10, day=1),
            frequency="weekly",
            end_datetime=datetime.datetime(year=2021, month=10, day=14),
            amount=-30
        ),
        Projection.Projection(
            name="monthly test",
            start_datetime=datetime.datetime(year=2020, month=10, day=1),
            frequency="monthly",
            end_datetime=datetime.datetime(year=2021, month=10, day=14),
            amount=1000
        ),
        Projection.Projection(
            name="yearly test",
            start_datetime=datetime.datetime(year=2020, month=10, day=1),
            frequency="yearly",
            end_datetime=datetime.datetime(year=2021, month=10, day=14),
            amount=-50
        ),
        Projection.Projection(
            name="monthly test",
            start_datetime=datetime.datetime(year=2019, month=10, day=1),
            frequency="weekly",
            end_datetime=datetime.datetime(year=2021, month=10, day=14),
            amount=-200
        ),
        # SalaryIncome.SalaryIncome(
        #     name="example income",
        #     yearly_income=60000,
        #     income_frequency="monthly",
        #     income_tax=.24,
        #     income_start=datetime.datetime(year=2021, month=8, day=1),
        #     income_end=datetime.datetime(year=2025, month=8, day=1),
        #     bonus=2000,
        #     bonus_frequency="yearly",
        #     bonus_tax=.30,
        #     bonus_start=datetime.datetime(year=2021, month=8, day=1),
        #     bonus_end=datetime.datetime(year=2025, month=8, day=1)
        # )
    ]

    # scenario_list = get_scenario_list()
    # scenario_list[-1].rewrite_projection_list(projection_list)


if __name__ == '__main__':
    main()
