import time
import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
from adafruit_ads1x15.ads1115 import ADS1115, P0

# Set up the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Set up the OLED display
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# Set up the ADS1115 ADC
ads = ADS1115(i2c)
chan = P0

# Create a blank image for drawing
width = oled.width
height = oled.height
image = Image.new("1", (width, height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

# Running text message
message = "Running text with ADS1115: "

try:
    while True:
        # Read analog value from ADS1115
        analog_value = ads[chan].value

        # Clear the image
        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        # Draw the text and analog value on the image
        draw.text((0, 0), message, font=font, fill=255)
        draw.text((0, 16), f"Analog Value: {analog_value}", font=font, fill=255)

        # Display the image
        oled.image(image)
        oled.show()

        # Pause for a short time
        time.sleep(0.5)

except KeyboardInterrupt:
    pass
finally:
    # Clear the display on exit
    oled.fill(0)
    oled.show()
