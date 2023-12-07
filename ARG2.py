import requests
from datetime import datetime, timezone
from gpiozero import Button
import subprocess
import time
import csv
import ping3
import paho.mqtt.client as mqtt
import json
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont


# Get ID Stations
id = "96607"
site = "ARG REK SAMARINDA"

# CSV log file
filename1 = 'data1menit.csv'
filename10 = 'data10menit.csv'
filenametemp = 'temp.csv'

#MQTT
broker_ip = "202.90.198.159"
broker_port = 1883
username = "bmkg_aws"
password = "bmkg_aws123"
topic = "device/KalTim/arg/96607"

# HTTP
url = "http://202.90.198.212/logger/write.php?dat="
host = "202.90.198.212"

print("..........STARTING ARG.........")
time.sleep(2)

# Counter
bucket = Button(17)  #GPIO pin connected to the tipping bucket rain gauge
tip_count = 0

def count_tips():
    global tip_count
    tip_count += 1

bucket.when_pressed = count_tips

date_utc = datetime.now(timezone.utc)
date = date_utc.strftime("%d%m%Y")

# Sensor tegangan
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
chan = AnalogIn(ads, ADS.P0)

# OLED
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

disp.fill(0)
disp.show()

width = disp.width
height = disp.height
image = Image.new("1", (width, height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

# Ambil baris terakhir data 1 menit
def get_line_1(filename1):
    try:
        with open(filename1, 'r') as file:
            reader = csv.reader(file)
            lines = list(reader)
            if len (lines) > 0:
                last_line = lines[-1]
                return last_line
    except csv.Error :
        print ("File not found")
    except FileNotFoundError:
        print ("File not found")
    except StopIteration:
        print ("File not found")

# Get last tip count
last_data1 = get_line_1(filename1)

if last_data1 == True:
    last_data = str(last_data1).replace("['", "").replace("']", "")
    last_data = last_data.split(";")
    last_date = str(last_data[1])
    last_date = last_date[:8]
    try:
        last_tip = float(last_data[2]) / 0.2
        last_tip = round(last_tip)
        last_tip = int(last_tip)

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
        RR = format(tip_count * 0.2, ".1f")

        # SUHU
        cpu_temp = str(get_cpu_temperature())
        
        # Volt Sensor
        voltage = chan.voltage
        volt = format(voltage * 5 , ".2f")

        # Pengumpulan data ke string
        data = id+";"+date_string+";"+RR+";"+cpu_temp+";"+volt+""

        # Display the voltage on the OLED
        text_width, _ = draw.textsize(data, font)
        x = width
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        draw.text((0, 0), f"DATA: {data}", font=font, fill=255)
        disp.image(image)
        disp.show()

        x -= 1
        if x < -text_width:
            x = width

        time.sleep(0.05)

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
            tanggal = dt_utc.strftime("%Y-%m-%d")
            jam = dt_utc.strftime("%H:%M:%S")
            message = {
                "date": tanggal,
                "time": jam,
                "id": id,
                "site": site,
                "rr": RR,
                "log_temp": cpu_temp
            }
            message = json.dumps(message)
            print(message)

            print("Data 1 menit:", data)
            time.sleep(1)
            write_to_csv1(data)
            time.sleep(1)
            send_MQTT(message)
            time.sleep(1)

        # Data 10 menit
        if dt_utc.minute % 10 == 0 and dt_utc.second == 0:
            print("Data 10 menit:", data)
            write_to_csv10(data)
            base_url = url + data
            time.sleep(1)
            result = koneksi(base_url)
            time.sleep(1)
            if result is True :
                print("........HTTP SEND.........")
            else :
                print(".........HTTP NOT SEND.........")
                # Simpan data gagal kirim ke csv
                write_to_csvtemp(data)
            time.sleep(1)

        # Reset tip count at midnight (UTC)
        if dt_utc.hour == 0 and dt_utc.minute == 0 and dt_utc.second == 30:
            reset_tip_count()

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
                    try :
                        time.sleep(1)
                        result = koneksi(base_url1)
                        if result is True:
                            print("...........PENGIRIMAN ULANG BERHASIL..........")
                            time.sleep(1)
                            delete_first_line_in_csv(filenametemp)
                        else:
                            print("..........PENGIRIMAN ULANG GAGAL..........")
                            #write_to_csvtemp(data)
                    except Exception as e:
                        print("SYSTEM ERROR : ", e)
                else:
                    print("..........GAGAL AMBIL DATA..........")
            else:
                print("..........DATA TIDAK DITEMUKAN..........")
        time.sleep(1)

except Exception as e:
    print("SYSTEM ERROR : ", e)