""" loads the server csv output and creates a table where
first column is a time axis and the following columns are 
data series; i.e. battery ID in a header followed by
 charge percentages """

import csv
from pathlib import Path
import time


def load_data(filename):
    print(f"Loading {filename}")
    with open(filename, "r", encoding="utf-8") as fp:
        reader = csv.reader(fp, delimiter=";")
        return list(reader)


def find_battery_count(data):
    """load IDs from first column, skip non-int remove duplicate, return max"""
    ids = [entry[0] for entry in data[1:]]
    for idx, id in enumerate(ids):
        try:
            ids[idx] = int(id)
        except ValueError:
            # not an int .. meh
            ids[idx] = 0
    max_id = max(set(ids))
    # -1 because first index is a timestamp
    print(f"Detected {len(set(ids)) - 1} battery IDs. Highest ID: {max_id}")
    return max_id


def extract_data(data):
    """take only Discharging entries and for each battery ID compile list of % values (index 14)"""
    batt_data = {}
    for row in data:
        # skip not discharging rows
        if not "Discharging" in row:
            continue
        try:
            row[0] = int(row[0])
        except ValueError:
            # invalid battery id .. skip row
            continue

        if row[0] not in batt_data.keys():
            batt_data[row[0]] = []

        batt_data[row[0]].append(int(row[14]))
    return batt_data


def transpose(matrix):
    """transpose the matrix, substitute missing with 0"""
    max_len = max([len(v) for _, v in matrix.items()])
    # len(matrix) + 1 => extra column for timestamp
    out = [[0] * (len(matrix) + 1) for i in range(max_len + 1)]
    timestamp = 0
    out[0][0] = "Timestamp"
    battery_order = list(matrix.keys())
    battery_order.sort()

    for batt_id, row in matrix.items():
        batt_column = battery_order.index(batt_id) + 1
        # write the battery ID on the first row
        out[0][batt_column] = batt_id

        for idx, value in enumerate(row):
            if value > 100:
                # handle measurement error
                value = ""
            out[idx + 1][batt_column] = value

            # timestamp for first column
            # update only if there is none
            if not out[idx + 1][0]:
                t = time.gmtime(timestamp)
                out[idx + 1][0] = f"{t.tm_hour:02}:{t.tm_min:02}:{t.tm_sec:02}"
                timestamp += 10

    return out


def write_data(data):
    """dump 2D list to file"""
    target = Path("batteries", "master.csv")
    print(f"Storing results in {target}")
    with open(target, "w", encoding="utf-8") as fp:
        writer = csv.writer(fp, delimiter=",", lineterminator="\n")
        writer.writerows(data)


data = load_data("battery_log.csv")
battery_count = find_battery_count(data)
print("Processing data")
extracted = extract_data(data)
output = transpose(extracted)
write_data(output)
