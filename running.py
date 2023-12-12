import time
import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_ads1x15.ads1115 as ADS

# Set up the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Set up the OLED display
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# Set up the ADS1115 ADC
#ads = AnalogIn(i2c, ADS.P0)

ads = ADS.ADS1115(i2c)

# Choose a channel on the ADC
chan = AnalogIn(ads, ADS.P0)

# Display dimensions
width = oled.width
height = oled.height

# Running text message
message = "Scrolling text with ADS1115: "

# Load a font
font = ImageFont.load_default()

# Create a blank image for drawing
image = Image.new("1", (width, height), 0)
draw = ImageDraw.Draw(image)

try:
    while True:
        # Read analog value from ADS1115
        analog_value = chan.value

        # Clear the display
        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        # Draw the scrolling text and analog value on the image
        x = 0
        y = (height - 8) // 2  # Assuming font height is 8 pixels
        draw.text((0, 0), message, font=font, fill=255)
        draw.text((0, y + 10), f"Analog: {analog_value}", font=font, fill=255)

        # Move the text to the left
        x -= 1

        # If the text has moved completely off the left side, reset its position
        if x < -len(message) * 8:
            x = width

        # Display the image on the OLED
        oled.image(image)
        oled.show()

        # Pause for a short time
        time.sleep(0.05)

except KeyboardInterrupt:
    pass
finally:
    # Clear the display on exit
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    oled.image(image)
    oled.show()
