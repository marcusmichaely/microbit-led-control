import tkinter as tk
import serial
import serial.tools.list_ports
import time

class LEDControl:
    def __init__(self, root):
        self.root = root
        self.root.title("Micro:bit LED Control")

        # Create status label
        self.status_frame = tk.Frame(root)
        self.status_frame.pack(pady=5)
        self.status_label = tk.Label(self.status_frame, text="Status: Not Connected", fg="red")
        self.status_label.pack()

        # Initialize serial connection
        self.serial = None
        self.connect_to_microbit()

        # Create main frame
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(padx=20, pady=20)

        # Create toggle button
        self.toggle_button = tk.Button(self.main_frame,
                                     text="Toggle LED",
                                     command=self.toggle_led,
                                     width=20,
                                     height=2)
        self.toggle_button.pack(pady=10)

        # Create connect button
        self.connect_button = tk.Button(self.main_frame,
                                      text="Connect to micro:bit",
                                      command=self.connect_to_microbit)
        self.connect_button.pack(pady=5)

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
                self.status_label.config(text=f"Status: Connected to {microbit_port}", fg="green")
                print(f"Connected to micro:bit on {microbit_port}")
            except Exception as e:
                self.serial = None
                self.status_label.config(text=f"Status: Connection failed - {str(e)}", fg="red")
                print(f"Failed to connect to micro:bit: {str(e)}")
        else:
            self.serial = None
            self.status_label.config(text="Status: No micro:bit found", fg="red")
            print("No micro:bit found. Please connect your micro:bit via USB.")

    def toggle_led(self):
        if self.serial is None:
            self.status_label.config(text="Status: Not connected to micro:bit", fg="red")
            return

        try:
            # Send '1' to toggle the LED
            self.serial.write(b'1\n')
            self.status_label.config(text="Status: Toggle command sent", fg="green")
        except Exception as e:
            self.status_label.config(text=f"Status: Failed to send - {str(e)}", fg="red")
            print(f"Error sending data to micro:bit: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LEDControl(root)
    root.mainloop()
