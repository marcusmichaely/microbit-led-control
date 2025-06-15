import serial
import serial.tools.list_ports
import time
import sys

class LEDControlCLI:
    def __init__(self):
        self.serial = None
        self.connect_to_microbit()
        self.running = True

    def connect_to_microbit(self):
        # Find micro:bit port
        ports = list(serial.tools.list_ports.comports())
        microbit_port = None

        for port in ports:
            if "micro:bit" in port.description.lower():
                microbit_port = port.device
                break

        if microbit_port:
            try:
                if self.serial:
                    self.serial.close()
                self.serial = serial.Serial(microbit_port, 115200, timeout=1)
                time.sleep(2)  # Wait for serial connection to establish
                print(f"✅ Connected to micro:bit on {microbit_port}")
                return True
            except Exception as e:
                self.serial = None
                print(f"❌ Failed to connect to micro:bit: {str(e)}")
                return False
        else:
            self.serial = None
            print("❌ No micro:bit found. Please connect your micro:bit via USB.")
            return False

    def toggle_led(self):
        if self.serial is None:
            print("❌ Not connected to micro:bit")
            return False

        try:
            # Send '1' to toggle the LED
            self.serial.write(b'1\n')
            print("✅ Toggle command sent")
            return True
        except Exception as e:
            print(f"❌ Error sending data to micro:bit: {str(e)}")
            return False

    def print_help(self):
        print("\nCommands:")
        print("  t - Toggle LED")
        print("  c - Connect to micro:bit")
        print("  h - Show this help message")
        print("  q - Quit")
        print()

    def run(self):
        print("Micro:bit LED Control (CLI Version)")
        print("==================================")
        self.print_help()

        while self.running:
            try:
                # Get user input
                cmd = input("Enter command (h for help): ").lower().strip()

                if cmd == 'q':
                    self.running = False
                    print("Goodbye!")
                elif cmd == 't':
                    self.toggle_led()
                elif cmd == 'c':
                    self.connect_to_microbit()
                elif cmd == 'h':
                    self.print_help()
                else:
                    print("❌ Unknown command. Type 'h' for help.")

            except KeyboardInterrupt:
                print("\nGoodbye!")
                self.running = False
            except Exception as e:
                print(f"❌ Error: {str(e)}")

        # Clean up
        if self.serial:
            self.serial.close()

if __name__ == "__main__":
    app = LEDControlCLI()
    app.run()
