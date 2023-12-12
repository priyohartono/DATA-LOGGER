import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADS1115 object
ads = ADS.ADS1115(i2c)

# Create an analog input channel on pin A0
chan = AnalogIn(ads, ADS.P0)

# Create the SSD1306 OLED class
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# Define the text to display
text = 'Welcome to my OLED display!'

# Scroll the text horizontally
for i in range(10):
    disp.clearDisplay()
    disp.setTextSize(1)
    disp.setTextColor(1, 1, 1)
    disp.drawString(0, 0, text)
    disp.display()
    time.sleep(0.1)
    disp.startScrollRight(0, 0, 128, 32)
    time.sleep(0.1)
    disp.stopScroll()

# Scroll the text vertically
for i in range(10):
    disp.clearDisplay()
    disp.setTextSize(1)
    disp.setTextColor(1, 1, 1)
    disp.drawString(0, 0, text)
    disp.display()
    time.sleep(0.1)
    disp.startScrollUp(0, 0, 128, 32)
    time.sleep(0.1)
    disp.stopScroll()