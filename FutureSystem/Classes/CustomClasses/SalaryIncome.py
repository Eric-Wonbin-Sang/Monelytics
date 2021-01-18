import datetime
import matplotlib.pyplot as plt

from FutureSystem.Classes import Projection


class SalaryIncome:

    def __init__(self, **kwargs):

        self.name = kwargs.get("name")
        self.yearly_income = kwargs.get("yearly_income")
        self.income_frequency = kwargs.get("income_frequency")
        self.income = self.get_income_amount()
        self.income_tax = kwargs.get("income_tax")
        self.income_start = kwargs.get("income_start")
        self.income_end = kwargs.get("income_end")

        self.bonus = kwargs.get("bonus")
        self.bonus_frequency = kwargs.get("bonus_frequency")
        self.bonus_tax = kwargs.get("bonus_tax")
        self.bonus_start = kwargs.get("bonus_start")
        self.bonus_end = kwargs.get("bonus_end")

        self.gross_income_dataframe = self.get_gross_income_dataframe()
        self.income_tax_dataframe = self.get_income_tax_dataframe()
        self.net_income_dataframe = self.get_net_income_dataframe()

        self.gross_bonus_dataframe = self.get_gross_bonus_dataframe()
        self.bonus_tax_dataframe = self.get_bonus_tax_dataframe()
        self.net_bonus_dataframe = self.get_net_bonus_dataframe()

        self.dataframe = self.get_net_dataframe()

    def get_income_amount(self):
        income_frequency = self.income_frequency
        if income_frequency == "bimonthly":
            return self.yearly_income / 24
        elif income_frequency == "monthly":
            return self.yearly_income / 12
        raise UserWarning("Unknown SalaryIncome income frequency '{}'".format(income_frequency))

    def get_gross_income_dataframe(self):
        gross_income_projection = Projection.Projection(
            name="Income",
            type="income",
            start_datetime=self.income_start,
            frequency=self.income_frequency,
            end_datetime=self.income_end,
            amount=self.income
        )
        return gross_income_projection.dataframe

    def get_income_tax_dataframe(self):
        income_tax_projection = Projection.Projection(
            name="Income Tax",
            type="expense",
            start_datetime=self.income_start,
            frequency=self.income_frequency,
            end_datetime=self.income_end,
            amount=self.income_tax
        )
        income_tax_dataframe = Projection.combine_projection_dfs(
            self.gross_income_dataframe,
            income_tax_projection.dataframe,
            amount_type="percent"
        )
        return income_tax_dataframe

    def get_net_income_dataframe(self):
        return Projection.combine_projection_dfs(
            self.gross_income_dataframe,
            self.income_tax_dataframe,
            amount_type="value"
        )

    def get_gross_bonus_dataframe(self):
        bonus_projection = Projection.Projection(
            name="Bonus",
            type="income",
            start_datetime=self.income_start,
            frequency=self.bonus_frequency,
            end_datetime=self.income_end,
            amount=self.bonus
        )
        return bonus_projection.dataframe

    def get_bonus_tax_dataframe(self):
        bonus_tax_projection = Projection.Projection(
            name="Bonus Tax",
            type="expense",
            start_datetime=self.income_start,
            frequency=self.bonus_frequency,
            end_datetime=self.income_end,
            amount=self.bonus_tax
        )
        return Projection.combine_projection_dfs(
            self.gross_bonus_dataframe,
            bonus_tax_projection.dataframe,
            amount_type="percent"
        )

    def get_net_bonus_dataframe(self):
        return Projection.combine_projection_dfs(
            self.gross_bonus_dataframe,
            self.bonus_tax_dataframe,
            amount_type="value"
        )

    def get_net_dataframe(self):
        return Projection.combine_projection_dfs(
            self.net_income_dataframe,
            self.net_bonus_dataframe,
            amount_type="value"
        )

    def plot(self):
        plt.plot(
            self.dataframe.index,
            self.dataframe["result"],
            alpha=0.8,
            marker="."
        )
