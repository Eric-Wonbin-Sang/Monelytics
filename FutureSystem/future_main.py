import os
import datetime
import pandas as pd

from FutureSystem.Classes import Projection, Scenario
from FutureSystem.Classes.ComplexProjections import SalaryIncome
from Classes import Profile

from General import Functions, Constants

pd.set_option('display.expand_frame_repr', False)


def get_scenario_list(profile):
    scenario_list = []
    for file_name in os.listdir(profile.scenarios_dir):
        file_path = profile.scenarios_dir + "/" + file_name
        scenario_list.append(Scenario.Scenario(profile, file_path))
    return scenario_list


def main():

    projection_list = [
        Projection.Projection(
            name="Initial Holdings",
            start_datetime=datetime.datetime(year=2021, month=5, day=1),
            frequency="yearly",
            end_datetime=datetime.datetime(year=2021, month=5, day=30),
            amount=16000
        ),




        Projection.Projection(
            name="Morgan Stanley - Starting Bonus",
            start_datetime=datetime.datetime(year=2021, month=7, day=15),
            frequency="yearly",
            end_datetime=datetime.datetime(year=2021, month=7, day=30),
            amount=10000
        ),
        Projection.Projection(
            name="Morgan Stanley - Gross Income",
            start_datetime=datetime.datetime(year=2021, month=8, day=15),
            frequency="biweekly",
            end_datetime=datetime.datetime(year=2026, month=5, day=2),
            amount=100000/26
        ),
        Projection.Projection(
            name="Morgan Stanley - Taxed Income",
            start_datetime=datetime.datetime(year=2021, month=8, day=15),
            frequency="biweekly",
            end_datetime=datetime.datetime(year=2026, month=5, day=2),
            amount=-100000/26 * .3
        ),
        Projection.Projection(
            name="Morgan Stanley - Yearly Bonus",
            start_datetime=datetime.datetime(year=2021, month=12, day=15),
            frequency="yearly",
            end_datetime=datetime.datetime(year=2026, month=12, day=15),
            amount=10000
        ),



        Projection.Projection(
            name="Job 2 - Starting Bonus",
            start_datetime=datetime.datetime(year=2026, month=7, day=1),
            frequency="yearly",
            end_datetime=datetime.datetime(year=2026, month=7, day=2),
            amount=30000
        ),
        Projection.Projection(
            name="Job 2 - Gross Income",
            start_datetime=datetime.datetime(year=2026, month=8, day=1),
            frequency="biweekly",
            end_datetime=datetime.datetime(year=2031, month=5, day=2),
            amount=170000 / 26
        ),
        Projection.Projection(
            name="Job 2 - Taxed Income",
            start_datetime=datetime.datetime(year=2026, month=8, day=1),
            frequency="biweekly",
            end_datetime=datetime.datetime(year=2031, month=5, day=2),
            amount=-170000 / 26 * .3
        ),
        Projection.Projection(
            name="Job 2 - Yearly Bonus",
            start_datetime=datetime.datetime(year=2026, month=12, day=15),
            frequency="yearly",
            end_datetime=datetime.datetime(year=2031, month=12, day=15),
            amount=10000
        ),





        Projection.Projection(
            name="Rent - 1st Apartment",
            start_datetime=datetime.datetime(year=2021, month=5, day=1),
            frequency="monthly",
            end_datetime=datetime.datetime(year=2026, month=5, day=1),
            amount=-1330
        ),
        Projection.Projection(
            name="Rent - 1st Apartment Utilities",
            start_datetime=datetime.datetime(year=2021, month=5, day=1),
            frequency="monthly",
            end_datetime=datetime.datetime(year=2026, month=5, day=1),
            amount=-1330 * .06
        ),
        Projection.Projection(
            name="Rent - 2nd Apartment",
            start_datetime=datetime.datetime(year=2021, month=5, day=1),
            frequency="monthly",
            end_datetime=datetime.datetime(year=2024, month=5, day=1),
            amount=-1600
        ),
        Projection.Projection(
            name="Rent - 2nd Apartment Utilities",
            start_datetime=datetime.datetime(year=2021, month=5, day=1),
            frequency="monthly",
            end_datetime=datetime.datetime(year=2024, month=5, day=1),
            amount=-1600 * .06
        ),
        Projection.Projection(
            name="Rent - 3rd Apartment",
            start_datetime=datetime.datetime(year=2024, month=5, day=1),
            frequency="monthly",
            end_datetime=datetime.datetime(year=2031, month=5, day=1),
            amount=-1800
        ),
        Projection.Projection(
            name="Rent - 3rd Apartment Utilities",
            start_datetime=datetime.datetime(year=2024, month=5, day=1),
            frequency="monthly",
            end_datetime=datetime.datetime(year=2031, month=5, day=1),
            amount=-1800 * .06
        ),



        Projection.Projection(
            name="LA Travel Expense",
            start_datetime=datetime.datetime(year=2021, month=5, day=1),
            frequency="monthly",
            end_datetime=datetime.datetime(year=2024, month=5, day=1),
            amount=-700
        ),




        Projection.Projection(
            name="Food Cost",
            start_datetime=datetime.datetime(year=2021, month=9, day=1),
            frequency="biweekly",
            end_datetime=datetime.datetime(year=2031, month=5, day=1),
            amount=-300
        ),
        Projection.Projection(
            name="Phone Plan",
            start_datetime=datetime.datetime(year=2021, month=5, day=1),
            frequency="monthly",
            end_datetime=datetime.datetime(year=2031, month=5, day=1),
            amount=-60
        ),
        Projection.Projection(
            name="Subscriptions",
            start_datetime=datetime.datetime(year=2021, month=5, day=1),
            frequency="monthly",
            end_datetime=datetime.datetime(year=2031, month=5, day=1),
            amount=-40
        ),
        Projection.Projection(
            name="Uncategorized Expenses",
            start_datetime=datetime.datetime(year=2021, month=5, day=1),
            frequency="monthly",
            end_datetime=datetime.datetime(year=2031, month=5, day=1),
            amount=-600
        ),
    ]

    profile_list = Profile.get_profile_list()
    main_profile = profile_list[0]

    run_cond = False
    if run_cond:
        Scenario.make_scenario_json(main_profile.scenarios_dir, "Scenario - Broad Life Projection.json")

    for i in range(2):
        scenario_list = get_scenario_list(main_profile)
        scenario_list[0].rewrite_projection_list(projection_list)
        print(scenario_list[0].create_graph())


if __name__ == '__main__':
    main()
