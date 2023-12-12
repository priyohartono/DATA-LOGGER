import time
import adafruit_ads1115
import adafruit_ssd1306

# Initialize the SSD1306 display
disp = adafruit_ssd1306.SSD1306(0x3C, 128, 32)

# Initialize the ADS1115 driver
ads = adafruit_ads1115.ADS1115()

# Set the I2C address of the ADS1115 driver
ads.set_i2c_addr(0x3C)

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