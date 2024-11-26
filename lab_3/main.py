import pandas as pd
import re

from checksum import *

# Чтение CSV
df = pd.read_csv("data.csv", sep=";", encoding="UTF-16")

# Регулярные выражения
email_regex = r'^\w+@\w+\.\w+'
height_regex = r'^[1-2]\.\d{2}$'
inn_regex = r'^\d{12}$'
passport_regex = r'^\d\d\s\d\d\s\d{6}$'
occupation_regex = r'[А-Я]+|[A-Z]+'
latitude_regex = r'^-?[1][1-8][1-9]\.\d+|^-?\d{1,2}\.\d+$'
hex_color_regex = r'^#[0-9a-f]{6}$'
issn_regex = r'^\d{4}-\d{4}$'
uuid_regex = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
time_regex = r'^[0-2]\d:[0-6]\d:[0-6]\d\.\d{6}$'

email_column = df.iloc[:, 0]
height_column = df.iloc[:, 1]
inn_column = df.iloc[:, 2]
passport_column = df.iloc[:, 3]
occupation_column = df.iloc[:, 4]
latitude_column = df.iloc[:, 5]
hex_color_column = df.iloc[:, 6]
issn_column = df.iloc[:, 7]
uuid_column = df.iloc[:, 8]
time_column = df.iloc[:, 9]

invalid_data = []


def search_invalid_data(regex, column):
    for index, value in column.items():
        if not re.match(regex, str(value)):
            invalid_data.append(index)


def search_all_invalid_data():
    search_invalid_data(email_regex, email_column)
    search_invalid_data(height_regex, height_column)
    search_invalid_data(inn_regex, inn_column)
    search_invalid_data(passport_regex, passport_column)
    search_invalid_data(occupation_regex, occupation_column)
    search_invalid_data(latitude_regex, latitude_column)
    search_invalid_data(hex_color_regex, hex_color_column)
    search_invalid_data(issn_regex, issn_column)
    search_invalid_data(uuid_regex, uuid_column)
    search_invalid_data(time_regex, time_column)


if __name__ == "__main__":
    search_all_invalid_data()
    serialize_result(7, calculate_checksum(invalid_data))

