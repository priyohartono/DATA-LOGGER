import requests
from datetime import datetime, timezone
from gpiozero import Button
import subprocess
import time
import csv
import ping3

# Get ID Stations
id = "ARGSMD"

# Counter
bucket = Button(17)  # GPIO pin connected to the tipping bucket rain gauge
tip_count = tip_count

def count_tips():
    global tip_count
    tip_count += 1

bucket.when_pressed = count_tips
print(tip_count)

# CSV log file
filename1 = 'data1menit.csv'
filename10 = 'data10menit.csv'
filenametemp = 'temp.csv'

# Reset counter
def reset_tip_count():
    global tip_count
    tip_count = 0
    print("Resetting tip count")

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
def get_first_line(filenametemp):
    with open(filenametemp, 'r') as file:
        # Create a CSV writer object
        reader = csv.reader(file)
        first_line = next(reader)
        return first_line

def delete_first_line_in_csv(filenametemp):
    with open(filenametemp, 'r') as file:
        lines = file.readlines()  # Read all lines into a list

    with open(filenametemp, 'w') as file:
        file.writelines(lines[1:])  # Write all lines except the first one

#Fungsi Utama
try:
    while True: 
        # Get the current UTC datetime
        dt_utc = datetime.now(timezone.utc)
        
        # Convert to a string
        date_string = dt_utc.strftime("%d%m%Y%H%M%S")
        
        # Convert tip_count to rainfall measurement using the specifications of your rain gauge
        rainfall = tip_count * 0.2
        rainfall = format(rainfall, ".1f")

        # Get RR
        RR = rainfall

        # SUHU
        cpu_temp = str(get_cpu_temperature())
        
        # Pengumpulan data ke string
        data = id+";"+date_string+";"+RR+";"+cpu_temp+";0.0"

        # Pengumpulan string data ke URL
        base_url = url + data
        #base_url1 = url + get_first_line(filenametemp)
        
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

        # Data 1 menit
        if dt_utc.second == 0:
            print("Data 1 menit:", data)
            write_to_csv1(data)
            time.sleep(1)

        # Data 10 menit
        if dt_utc.minute % 10 == 0 and dt_utc.second == 0:
            print("Data 10 menit:", data)
            write_to_csv10(data)
            result = koneksi(base_url)
            if result is True :
                print("Data terkirim")
            else :
                print("Data tidak terkirim")
                # Simpan data gagal kirim ke csv
                write_to_csvtemp(data)
            print(koneksi)
            time.sleep(1)

        # Reset tip count at midnight (UTC)
        if dt_utc.hour == 0 and dt_utc.minute == 0 and dt_utc.second == 5:
            reset_tip_count()
            time.sleep(1)

        # Pengiriman ulang data gagal kirim
        #if dt_utc.hour % 1 == 0 and dt_utc.minute == 5 and dt_utc.second == 0:
        
        if dt_utc.minute % 10 == 5 and dt_utc.second == 0:
            check_temp_file
            print("..........SCAN DATA GAGAL KIRIM..........")
            if check_temp_file(filenametemp):
                print("..........DATA DITEMUKAN..........")
                ping_server
                if ping_server:
                    print("..........AMBIL DATA GAGAL KIRIM..........")
                    get_first_line(filenametemp)
                    data_gagal = str(get_first_line(filenametemp)).replace("['","").replace("']","")
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