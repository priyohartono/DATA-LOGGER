import time
import board
import busio
import adafruit_ssd1306
from adafruit_ads1x15.analog_in import AnalogIn, P0

# Set up the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Set up the OLED display
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# Set up the ADS1115 ADC
ads = AnalogIn(i2c, P0)

# Display dimensions
width = oled.width
height = oled.height

# Running text message
message = "Scrolling text with ADS1115: "

# Create a framebuffer for the display
buffer = bytearray((width // 8) * height)
framebuf = adafruit_ssd1306.FrameBuffer(buffer, width, height, adafruit_ssd1306.MonoMode)

try:
    while True:
        # Read analog value from ADS1115
        analog_value = ads.value

        # Clear the display
        framebuf.fill(0)

        # Draw the scrolling text and analog value on the framebuffer
        x = width
        y = (height - 8) // 2  # Assuming font height is 8 pixels

        framebuf.text(message, x, y, 1)
        framebuf.text(f"Analog: {analog_value}", 0, y + 10, 1)

        # Move the text to the left
        x -= 1

        # If the text has moved completely off the left side, reset its position
        if x < -len(message) * 8:
            x = width

        # Transfer the framebuffer to the display
        oled.framebuf.blit(framebuf, 0, 0)
        oled.show()

        # Pause for a short time
        time.sleep(0.05)

except KeyboardInterrupt:
    pass
finally:
    # Clear the display on exit
    oled.fill(0)
    oled.show()
