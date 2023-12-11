import time
import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

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

# Load a font (choose an appropriate size)
font = ImageFont.load_default()

# Running text message
message = "This is a running text example for a 128x32 OLED display. "

try:
    while True:
        # Clear the image
        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        # Draw the text on the image
        draw.text((width, (height - font.getsize(message)[1]) // 2), message, font=font, fill=255)

        # Display the image
        disp.image(image)
        disp.show()

        # Move the text to the left
        width -= 1

        # If the text has moved completely off the left side, reset its position
        if width < -font.getsize(message)[0]:
            width = disp.width

        # Pause for a short time
        time.sleep(0.05)

except KeyboardInterrupt:
    pass
finally:
    # Clear the display on exit
    disp.fill(0)
    disp.show()
