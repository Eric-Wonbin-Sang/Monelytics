import os
import csv
import json
import codecs
import pickle
import calendar
import datetime
import itertools


def pickle_this(some_variable, file_path):
    pickle.dump(some_variable, open(file_path, "wb"))


def unpickle(file_path):
    return pickle.load(open(file_path, "rb"))


def get_path_list_in_dir(some_dir):
    return [
        (some_dir + "/" + path).replace("\\", "/") for path in os.listdir(some_dir)
    ]


def get_curr_parent_dir():
    # return "/".join(os.path.dirname(os.getcwd()).replace("\\", "/").split("/")[:-1])
    return "C:/Users/ericw/CodingProjects"


def csv_to_list_list(csv_path):
    types_of_encoding = ["utf8", "cp1252"]
    for encoding_type in types_of_encoding:
        with codecs.open(csv_path, encoding=encoding_type, errors='replace') as csv_file:
            data_list_list = []
            for row in csv.reader(csv_file, delimiter=','):
                data_list_list.append(row)
            return data_list_list


def make_combos(data_list, group_amt):
    return itertools.combinations(data_list, group_amt)


def remove_empty_lists(data_list_list):
    ret_list_list = []
    for data_list in data_list_list:
        if data_list:
            ret_list_list.append(data_list)
    return ret_list_list


def get_col(data_list_list, col_index):
    return [data_list[col_index] for data_list in data_list_list]


def get_first_in_list(data_list):
    for data in data_list:
        if data is not None and data != "":
            return data
    return None


def parse_json(json_path):
    if not os.path.exists(json_path):
        raise FileExistsError
    with open(json_path) as f:
        return json.load(f)


def dict_to_json(data_dict, file_path):
    with open(file_path, 'w') as file:
        json.dump(data_dict, file)


def str_to_length(base_str, length, do_dots=True, do_left=True):
    base_str = str(base_str)
    if do_left:
        ret_str = base_str.ljust(length)[:length]
        if do_dots and len(base_str) + 3 > length:
            return ret_str[:-3] + "..."
    else:
        ret_str = base_str.rjust(length)[:length]
        if do_dots and len(base_str) + 3 > length:
            return "..." + ret_str[3:]
    return ret_str


def list_list_to_str(data_list_list, str_length=20):
    return "\n".join([" ".join([str_to_length(x, str_length) for x in data_list]) for data_list in data_list_list])


def tab_str(data_str, tab_amount):
    return ("\t" * tab_amount) + data_str.replace("\n", "\n" + ("\t" * tab_amount))


def dataframe_to_str(dataframe, str_length=20, spacer=" | "):
    ret_str = spacer.join([str_to_length(x, str_length) for x in dataframe.columns]) + "\n"
    ret_str += "\n".join([spacer.join([str_to_length(x, str_length) for x in list(data_list)]) for data_list in dataframe.values])
    return ret_str


def add_months(source_date, months):
    month = source_date.month - 1 + months
    year = source_date.year + month // 12
    month = month % 12 + 1
    day = min(source_date.day, calendar.monthrange(year, month)[1])
    return datetime.datetime(year, month, day)


def wait_for_temp_file(some_dir, second_limiter, type_specifier=".csv"):
    base_time = datetime.datetime.now()
    while (datetime.datetime.now() - base_time).seconds < second_limiter:
        for path in os.listdir(some_dir):
            if path.endswith(type_specifier):
                return some_dir + "\\" + path


def df_to_str(some_df):
    statement_df = some_df.copy()

    if statement_df.empty:
        return "empty dataframe"

    index_length = 23
    col_length = 20

    statement_df.index = statement_df.index.map(lambda x: str_to_length(x, index_length, do_dots=True, do_left=True))
    statement_df = statement_df.applymap(lambda x: str_to_length(x, col_length, do_dots=True, do_left=True))
    statement_df.columns = statement_df.columns.map(lambda x: str_to_length(x, col_length, do_dots=True, do_left=True))
    return statement_df.to_string()


def clean_money_str(some_str):
    return round(float(some_str.replace("$", "").replace("+", "").replace(" ", "").replace(",", "")), 2)
