import os
import pandas
import plotly.graph_objects as go

from FutureSystem.Classes import Projection

from General import Functions, Constants


class Scenario:

    def __init__(self, scenario_json_path):

        self.scenario_json_path = scenario_json_path
        self.name = self.get_name()

        self.projection_dict_list = Functions.parse_json(self.scenario_json_path)
        self.projection_list = [Projection.json_dict_to_projection(p_d) for p_d in self.projection_dict_list]
        self.complete_df = self.get_complete_df()

        self.create_graph()

    def get_name(self):
        return self.scenario_json_path.split("/")[-1].split(" - ")[-1][:-5]

    def rewrite_projection_list(self, projection_list):
        if os.path.exists(self.scenario_json_path):
            os.remove(self.scenario_json_path)
        Functions.dict_to_json(
            [projection.to_dict() for projection in projection_list],
            self.scenario_json_path
        )

    def get_complete_df(self):

        # datetime_list = pd.date_range(
        #     start=datetime.datetime(year=2020, month=10, day=14),
        #     periods=365 * 6
        # ).to_pydatetime().tolist()

        dataframe_list = []
        for projection in self.projection_list:
            dataframe_list.append(
                projection.dataframe.rename(columns={"result": "{} result".format(projection.name)})
            )

        if not dataframe_list:
            return None

        complete_df = pandas.concat(dataframe_list)
        complete_df = complete_df.sort_index()

        copy_df = complete_df.where(pandas.notnull(complete_df), 0)
        copy_df["result"] = copy_df.sum(axis=1)

        delta_list = []
        for value in copy_df["result"]:
            if not delta_list:
                delta_list.append(value)
            else:
                delta_list.append(value + delta_list[-1])
        complete_df["result"] = delta_list
        return complete_df

    def create_graph(self):
        fig = go.Figure()
        for projection in self.projection_list:
            fig.add_trace(go.Scatter(
                x=projection.dataframe.index,
                y=[float(data) for data in projection.dataframe["result"]],
                mode='lines+markers',
                name=projection.name)
            )

        if self.complete_df is not None:
            fig.add_trace(go.Scatter(
                x=self.complete_df.index,
                y=[float(data) for data in self.complete_df["result"]],
                mode='lines+markers',
                name="complete_df")
            )

        fig.update_layout(
            # template='simple_white',
            xaxis_title='Time',
            yaxis_title='Amount',
            title=self.name + ' - Projections',
            hovermode="x",
            legend={
                "yanchor": "top",
                "y": 0.99,
                "xanchor": "left",
                "x": 0.01
            }
        )

        fig.write_html(Constants.future_system_graph_path)
        return Constants.future_system_graph_path

    def to_dict(self):
        return {
            "scenario_json_path": self.scenario_json_path,
            "name": self.name,
            "projection_dict_list": [projection.to_dict() for projection in self.projection_list]
        }

    def __str__(self):
        ret_str = ""
        for i, projection in enumerate(self.projection_list):
            if i != 0:
                ret_str += "\n"
            ret_str += str(projection)
        ret_str = "\t" + ret_str.replace("\n", "\n\t")
        return "Scenario: {}\n".format(self.name) + ret_str


def create_empty_scenario(scenario_name):
    Functions.dict_to_json([], Constants.scenarios_dir + "/" + "Scenario - {}.json".format(scenario_name))
