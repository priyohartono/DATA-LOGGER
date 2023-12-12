import time
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas

# Set up the OLED display
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)

# Running text message
message = "Scrolling text on OLED: "
font_width = 16  # Assuming font width is 8 pixels

try:
    while True:
        # Scroll the text to the left
        for i in range(len(message) * font_width + device.width):
            with canvas(device) as draw:
                draw.text((-i, 0), message, fill="white")

            # Pause for a short time
            time.sleep(0.05)

except KeyboardInterrupt:
    pass
finally:
    # Clear the display on exit
    with canvas(device) as draw:
        draw.text((0, 0), " ", fill="black")
