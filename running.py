from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont
import time

# Set up the serial interface
serial = i2c(port=1, address=0x3C)

# Set up the OLED display
device = ssd1306(serial, rotate=0)

# Create a blank image for drawing
width = device.width
height = device.height
image = Image.new("1", (width, height))
draw = ImageDraw.Draw(image)

# Load a font
font = ImageFont.load_default()

# Running text message
message = "This is a running text example for OLED display."

# Calculate text width for scrolling
text_width, _ = draw.textlength(message, font)

# Initialize starting position
x = width

try:
    while True:
        # Draw the text on the image
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        draw.text((x, (height - font.getsize(message)[1]) // 2), message, font=font, fill=255)

        # Display the image
        device.display(image)

        # Scroll the text
        x -= 1
        if x < -text_width:
            x = width

        # Pause for a short time
        time.sleep(0.05)

except KeyboardInterrupt:
    pass
finally:
    # Clear the display on exit
    device.clear()
