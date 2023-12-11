import time
import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the SSD1306 OLED class
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# Create a blank image for drawing
width = disp.width
height = disp.height
image = Image.new("1", (width, height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

# Create the ADC object
ads = ADS.ADS1115(i2c)
analog_in = AnalogIn(ads, ADS.P0)  # Change to the appropriate analog input

try:
    while True:
        # Clear the image
        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        # Read analog value from ADS1115
        analog_value = analog_in.value
        voltage = analog_in.voltage

        # Display the analog value on OLED
        message = f"Analog Value: {analog_value}\nVoltage: {voltage:.2f} V"
        draw.text((0, 0), message, font=font, fill=255)

        # Display the image
        disp.image(image)
        disp.show()

        # Pause for a short time
        time.sleep(1)

except KeyboardInterrupt:
    pass
finally:
    # Clear the display on exit
    disp.fill(0)
    disp.show()
