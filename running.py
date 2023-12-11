import time
import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Set up the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Set up the OLED display
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# Set up the ADS1115 ADC
ads = ADS.ADS1115(i2c)
chan = AnalogIn(ads, ADS.P0)

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
        analog_value = chan.value

        # Clear the image
        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        # Draw the text and analog value on the image
        draw.text((0, 0), message, font=font, fill=255)
        draw.text((0, 16), f"Analog Value: {analog_value}", font=font, fill=255)

        # Display the image
        oled.image(image)
        oled.show()

        # Move the text to the left
        width -= 1

        # If the text has moved completely off the left side, reset its position
        if width < -font.getlength(message)[0]:
            width = oled.width

        # Pause for a short time
        time.sleep(0.5)

except KeyboardInterrupt:
    pass
finally:
    # Clear the display on exit
    oled.fill(0)
    oled.show()
