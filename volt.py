import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)

# Choose a channel on the ADC
channel = AnalogIn(ads, ADS.P0)

# Main loop
try:
    while True:
        # Read the voltage and print it
        voltage = channel.voltage
        print(f"Voltage: {voltage}V")
        time.sleep(1)

except KeyboardInterrupt:
    pass
