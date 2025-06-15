# micro:bit LED toggle receiver
from microbit import *

# Initialize the display
display.clear()

# Set initial LED state
led_state = False

while True:
    if uart.any():  # Check if there's any data to read
        try:
            # Read the incoming data
            data = uart.readline().decode('utf-8').strip()

            # Toggle the LED state if we receive '1'
            if data == '1':
                led_state = not led_state
                # Update the display
                display.set_pixel(2, 2, 9 if led_state else 0)

        except Exception as e:
            # If there's an error, show an X pattern
            display.show(Image.NO)
            sleep(1000)
            display.clear()
