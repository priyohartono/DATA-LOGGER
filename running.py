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
ads = AnalogIn(i2c, ADS.P0)

# Create a blank image for drawing
width = oled.width
height = oled.height
image = Image.new("1", (width, height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

# Running text message
message = "Scrolling text with ADS1115: "

try:
    while True:
        # Read analog value from ADS1115
        analog_value = ads.value

        # Clear the image
        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        # Draw the scrolling text and analog value on the image
        text_width, text_height = draw.textsize(message, font=font)
        x = width
        y = (height - text_height) // 2
        draw.text((x, y), message, font=font, fill=255)

        # Move the text to the left
        x -= 1

        # If the text has moved completely off the left side, reset its position
        if x < -text_width:
            x = width

        # Display the image
        oled.image(image)
        oled.show()

        # Pause for a short time
        time.sleep(0.05)

except KeyboardInterrupt:
    pass
finally:
    # Clear the display on exit
    oled.fill(0)
    oled.show()
