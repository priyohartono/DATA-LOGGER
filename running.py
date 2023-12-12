import time
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas

# Set up the OLED display
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)

# Running text message
message = "Scrolling text on OLED: "

try:
    while True:
        # Clear the display
        with canvas(device) as draw:
            draw.text((0, 16), message, fill="white")

        # Pause for a short time
        time.sleep(0.5)

        # Scroll the text to the left
        for i in range(len(message) * 8 + 1):
            with canvas(device) as draw:
                draw.text((-i, 16), message, fill="white")

            # Pause for a short time
            time.sleep(0.05)

except KeyboardInterrupt:
    pass
finally:
    # Clear the display on exit
    with canvas(device) as draw:
        draw.text((0, 16), " ", fill="black")
