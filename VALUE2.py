import csv
from datetime import datetime, timezone
import os

filename1 = 'data1.csv'
dt_utc = datetime.now(timezone.utc)
date = dt_utc.strftime("%d%m%Y")

print(date)

def get_first_line(filename1):
    try:
        with open(filename1, 'r') as file:
            reader = csv.reader(file)
            first_line = next(reader)
            return first_line
    except FileNotFoundError:
        return None
    except StopIteration:
        return None

# Get the first line from the CSV file
first_line_data = get_first_line(filename1)

if first_line_data:
    last_data = str(first_line_data).replace("['", "").replace("']", "")
    last_data = last_data.split(";")

    last_date = str(last_data[1])
    last_date = last_date[:8]
    print(last_date)

    try:
        RR = float(last_data[2]) / 0.2
        RR = int(RR)
        print(RR)

        if last_date == date:
            tip = RR
        else:
            tip = 0

        print(tip)
    except IndexError:
        tip = 0
else:
    tip = 0
