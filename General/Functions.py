import itertools
import csv
import codecs


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
