import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Set up the OLED display
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# Create the ADS1115 object
ads = ADS.ADS1115(i2c)

# Create an analog input channel on pin A0
chan = AnalogIn(ads, ADS.P0)

# Create the SSD1306 OLED class
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# Clear the display
disp.fill(0)
disp.show()

# Create a blank image for drawing
width = disp.width
height = disp.height
image = Image.new("1", (width, height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

try:
    while True:
        # Read the analog voltage
        voltage = chan.voltage
        volt = voltage * 5

        # Display the voltage on the OLED
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        draw.text((0, 0), f"Voltage: {volt:.2f}V", font=font, fill=255)
        disp.image(image)
        disp.show()

        time.sleep(1)

except KeyboardInterrupt:
    pass
