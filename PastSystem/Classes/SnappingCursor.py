import datetime
import pandas as pd
import math
import matplotlib.dates as mdates


class SnappingCursor:
    """
    A cross hair cursor that snaps to the data point of a line, which is
    closest to the *x* position of the cursor.

    For simplicity, this assumes that *x* values of the data are sorted.
    """
    def __init__(self, ax, line_list, full_database):
        self.ax = ax
        self.full_database = full_database
        years_fmt = mdates.DateFormatter('%Y/%m/%d')
        self.ax.xaxis.set_major_formatter(years_fmt)
        self.line_list = line_list

        self.horizontal_line = self.get_horizontal_line()
        self.vertical_line = self.get_vertical_line()
        self.text = self.get_text()

        self.x_list, self.y_list = self.line_list[0].get_data()

        self.x_list_list, self.y_list_list = self.get_x_and_y_list_list()

        self._last_index = None

    def get_horizontal_line(self):
        horizontal_line = self.ax.axhline(color='k', lw=0.8, ls='--')
        horizontal_line.set_visible(False)
        return horizontal_line

    def get_vertical_line(self):
        vertical_line = self.ax.axvline(datetime.datetime(2019, 9, 21), color='k', lw=0.8, ls='--')
        vertical_line.set_visible(False)
        return vertical_line

    def get_text(self):
        text = self.ax.text(0.72, 0.9, 'Test', transform=self.ax.transAxes)
        return text

    def get_x_and_y_list_list(self):
        x_list_list, y_list_list = [], []
        for line in self.line_list:
            x_list, y_list = line.get_data()
            x_list = [datetime.datetime.fromtimestamp(x.astype('O')/1e9) for x in x_list]
            x_list_list.append(x_list)
            y_list_list.append(y_list)
        return x_list_list, y_list_list

    def set_cross_hair_visible(self, visible):
        need_redraw = self.horizontal_line.get_visible() != visible
        self.horizontal_line.set_visible(visible)
        self.vertical_line.set_visible(visible)
        self.text.set_visible(visible)
        return need_redraw

    def on_mouse_move(self, event):
        if not event.inaxes:
            self._last_index = None
            need_redraw = self.set_cross_hair_visible(False)
            if need_redraw:
                self.ax.figure.canvas.draw()
        else:
            curr_x = datetime.datetime(*[int(x) for x in self.ax.format_xdata(event.xdata).split("/")])
            curr_y = float(self.ax.format_ydata(event.ydata))

            min_col_name, min_values = None, None

            second_spread = 60*60*12
            value_spread = 100

            filtered_dataframe = self.full_database.loc[
                curr_x - datetime.timedelta(seconds=second_spread):curr_x + datetime.timedelta(seconds=second_spread)]
            # filtered_dataframe = filtered_dataframe[filtered_dataframe < curr_y - value_spread].dropna()
            # filtered_dataframe = filtered_dataframe[filtered_dataframe > curr_y + value_spread]

            for col_name in filtered_dataframe:
                series = filtered_dataframe[col_name]
                date_list = []
                value_list = []
                for i, value in enumerate(series.tolist()):
                    if value and curr_y - value_spread < value < curr_y + value_spread:
                        date_list.append(series.index[i])
                        value_list.append(value)
                # date_list = series.index
                # value_list = series.tolist()

                distance_list = [math.sqrt((curr_x - date_list[i]).seconds ** 2 + (curr_y - value_list[i]) ** 2)
                                 for i in range(len(date_list))]
                print(distance_list)

                if distance_list:
                    min_index = distance_list.index(min(distance_list))
                    if min_col_name is None:
                        min_col_name = col_name
                        min_values = [value_list[min_index], date_list[min_index], value_list[min_index]]
                    else:
                        if min_values[0] > value_list[min_index]:
                            min_col_name = col_name
                            min_values = [value_list[min_index], date_list[min_index], value_list[min_index]]

            if min_values:
                self.set_cross_hair_visible(True)
                self.vertical_line.set_xdata(min_values[1])
                self.horizontal_line.set_ydata(min_values[2])

                self.text.set_text('{}\nx={}, y={}'.format(min_col_name, min_values[1], min_values[2]))
            else:
                self.set_cross_hair_visible(False)

            self.ax.figure.canvas.draw()
