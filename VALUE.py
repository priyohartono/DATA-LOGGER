import csv
from datetime import datetime, timezone

filename1 = 'data1.csv'
dt_utc = datetime.now(timezone.utc)
date = dt_utc.strftime("%d%m%Y")

print(date)

def get_first_line(filename1):
    with open(filename1, 'r') as file:
        # Create a CSV writer object
        reader = csv.reader(file)
        first_line = next(reader)
        return first_line
    
last_data = str(get_first_line(filename1)).replace("['","").replace("']","")
last_data = last_data.split(";")

last_date = str(last_data[1])
last_date = last_date[:8]
print(last_date)

RR = float(last_data[2])/0.2
RR = int(RR)
print (RR)

if last_date == date :
    tip = RR
else :
    tip = 0

print (tip)