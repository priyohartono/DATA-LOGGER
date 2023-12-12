import time
import machine
from ssd1306 import SSD1306_I2C
import Adafruit_SSD1306
import Adafruit_ADS1115

# Initialize the SSD1306 display
disp = Adafruit_SSD1306.SSD1306_128_32(0x3C)

# Initialize the ADS1115 driver
ads = Adafruit_ADS1115.ADS1115()

# Set the I2C address of the ADS1115 driver
ads.set_i2c_addr(0x3C)

# Define the text to display
text = 'Welcome to my OLED display!'

# Scroll the text horizontally
for i in range(10):
    disp.fill()
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