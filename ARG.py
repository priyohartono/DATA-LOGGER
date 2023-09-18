import requests
from datetime import datetime, timezone
from gpiozero import Button
import subprocess
import time
import csv
import ping3
import paho.mqtt.client as mqtt

print("..........STARTING ARG.........")
time.sleep(2)

# Get ID Stations
id = "ARGSMD"

# CSV log file
filename1 = 'data1menit.csv'
filename10 = 'data10menit.csv'
filenametemp = 'temp.csv'
filenamevalue = 'lastvalue.csv'

#MQTT
broker_ip = "202.90.198.159"
broker_port = 1883
username = "bmkg_aws"
password = "bmkg_aws123"
topic = "device/KalTim/arg/smd"

# Counter
bucket = Button(17)  # GPIO pin connected to the tipping bucket rain gauge
tip_count = 0

def count_tips():
    global tip_count
    tip_count += 1

bucket.when_pressed = count_tips

date_utc = datetime.now(timezone.utc)
date = date_utc.strftime("%d%m%Y")

# Ambil baris terakhir data 1 menit
def get_last_value(filenamevalue):
    try:
        with open(filenamevalue, 'r') as file:
            reader = csv.reader(file)
            lines = list(reader)
            if len (lines) > 0:
                last_line = lines[-1]
                return last_line
    except FileNotFoundError:
        return None
    except StopIteration:
        return None

# Get last tip count
last_data1 = get_last_value(filenamevalue)
print(last_data1)

if last_data1:
    last_data = str(last_data1).replace("['", "").replace("']", "")
    last_data = last_data.split(";")
    print(last_data)
    last_date = str(last_data[1])
    last_date = last_date[:8]
    print(last_date)

    try:
        last_tip = float(last_data[2]) / 0.2
        last_tip = round(last_tip)
        last_tip = int(last_tip)
        print(last_tip)

        if last_date == date:
            tip_count = last_tip
        else:
            tip_count = 0

    except IndexError:
        tip_count = 0
else:
    tip_count = 0

# Reset counter
def reset_tip_count():
    global tip_count
    tip_count = 0
    print("Resetting RR")

# URL
url = "http://202.90.198.212/logger/write.php?dat="
host = "202.90.198.212"

#Suhu CPU
def get_cpu_temperature():
    command = "vcgencmd measure_temp"
    result = subprocess.check_output(command, shell=True)
    temperature = result.decode("utf-8")
    temperature = temperature.replace("temp=", "").replace("'C\n", "")
    return float(temperature)

# Cek Jaringan
def ping_server(host):
    try:
        response_time = ping3.ping(host)
        if response_time is not None and response_time is not False:
            return True
        else:
            return False
        
    except Exception as e:
        print("Error:", e)

ping_server(host)

if ping_server(host) == True:
    print("..........BERHASIL PING SERVER..........")
else:
    print("..........GAGAL PING SERVER..........")

# Pengiriman ke HTTP SERVER
def koneksi(url):
    try:
        r = requests.get(url, timeout = 10)
        return r.status_code >= 200 and r.status_code < 300
    except requests.exceptions.RequestException:
        return False
    
# Cek data gagal kirim
def check_temp_file(filenametemp):
    # Open the CSV file in read mode
    with open(filenametemp, 'r') as file:
        # Create a CSV reader object
        reader = csv.reader(file)
        # Check if the CSV file has any rows
        has_rows = any(reader)
    return has_rows

# Ambil baris pertama pada data gagal kirim
def get_line_temp(filenametemp):
    with open(filenametemp, 'r') as file:
        # Create a CSV writer object
        reader = csv.reader(file)
        first_line = next(reader)
        return first_line

# Hapus data berhasil kirim ulang
def delete_first_line_in_csv(filenametemp):
    with open(filenametemp, 'r') as file:
        lines = file.readlines()  # Read all lines into a list
    with open(filenametemp, 'w') as file:
        file.writelines(lines[1:])  # Write all lines except the first one

#MQTT
def send_MQTT(message):
    try:
        client = mqtt.Client()
        client.username_pw_set(username,password)
        client.connect(broker_ip,broker_port)
        client.publish(topic, message)
        print("MQTT SEND")
    except Exception as e:
        print("Error MQTT", str(e))

#Fungsi Utama
try:
    while True: 
        # Get the current UTC datetime
        dt_utc = datetime.now(timezone.utc)
        
        # Convert to a string
        date_string = dt_utc.strftime("%d%m%Y%H%M%S")

        # Convert tip_count to rainfall measurement using the specifications of your rain gauge
        RR = tip_count * 0.2
        RR = format(RR, ".1f")

        # SUHU
        cpu_temp = str(get_cpu_temperature())
        
        # Pengumpulan data ke string
        data = id+";"+date_string+";"+RR+";"+cpu_temp+""

        # Pengumpulan string data ke URL
        base_url = url + data

        # Message MQTT
        message = data
        
        # Fungsi CSV 1 menit
        def write_to_csv1(data):
            with open(filename1, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([data])
        
        # Fungsi CSV 10 menit
        def write_to_csv10(data):
            with open(filename10, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([data])

        # Fungsi CSV data gagal kirim
        def write_to_csvtemp(data):
            with open(filenametemp, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([data])

        # Tambah data ke last value
        def add_to_lastvalue(filenamevalue, data):
            with open(filenamevalue, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for row in data:
                    writer.writerow(row)

        # Limit 10 line
        def append_to_csv(filenamevalue, new_value):
            data = get_last_value(filenamevalue)
            # Append the new line
            data.append(new_value)
            # Check line count and remove the first line if needed
            if len(data) > 10:
                data.pop(0)
            # Write the updated data to the CSV file
            add_to_lastvalue(filenamevalue, data)

        new_value = data
        append_to_csv(filenamevalue, new_value)

        # Data 1 menit
        if dt_utc.second == 0:
        #if dt_utc.minute % 1 == 0 and dt_utc.second == 0:
            print("Data 1 menit:", data)
            write_to_csv1(data)
            send_MQTT(data)
            time.sleep(1)

        # Data 10 menit
        if dt_utc.minute % 10 == 0 and dt_utc.second == 0:
            print("Data 10 menit:", data)
            write_to_csv10(data)
            result = koneksi(base_url)
            if result is True :
                print("........HTTP SEND.........")
            else :
                print(".........HTTP NOT SEND.........")
                # Simpan data gagal kirim ke csv
                write_to_csvtemp(data)
            time.sleep(1)

        # Reset tip count at midnight (UTC)
        if dt_utc.hour == 0 and dt_utc.minute == 0 and dt_utc.second == 5:
            reset_tip_count()
            time.sleep(1)

        # Pengiriman ulang data gagal kirim       
        if dt_utc.minute % 10 == 5 and dt_utc.second == 0:
            check_temp_file
            print("..........SCAN DATA GAGAL KIRIM..........")
            if check_temp_file(filenametemp):
                print("..........DATA DITEMUKAN..........")
                ping_server
                if ping_server:
                    print("..........AMBIL DATA GAGAL KIRIM..........")
                    get_line_temp(filenametemp)
                    data_gagal = str(get_line_temp(filenametemp)).replace("['","").replace("']","")
                    base_url1 = url + data_gagal
                    print(base_url1)
                    try :
                        result = koneksi(base_url1)
                        if result is True:
                            print("...........PENGIRIMAN ULANG BERHASIL..........")
                            delete_first_line_in_csv(filenametemp)
                        else:
                            print("..........PENGIRIMAN ULANG GAGAL..........")
                    except Exception as e:
                        print("SYSTEM ERROR : ", e)
                else:
                    print("..........GAGAL AMBIL DATA..........")
            else:
                print("..........DATA TIDAK DITEMUKAN..........")
        time.sleep(1)

except Exception as e:
    print("SYSTEM ERROR : ", e)