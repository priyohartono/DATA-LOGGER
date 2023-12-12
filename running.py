import time
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306

# Set up the OLED display
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)

# Running text message
message = "Scrolling text on OLED: Hello, World! "

try:
    while True:
        # Scroll the text to the left
        for i in range(len(message) * 8 + device.width):
            with device as draw:
                draw.text((-i, 0), message, fill="white")

            # Pause for a short time
            time.sleep(0.05)

except KeyboardInterrupt:

