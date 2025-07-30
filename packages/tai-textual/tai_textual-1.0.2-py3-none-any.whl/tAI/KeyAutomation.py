import time
import subprocess
from pynput.keyboard import Controller, Key

class Automate():
    def __init__(self):
        self.command = None
        self.keyboard = Controller()

    def paste_command_to_terminal(self, command: str) -> None:
        """Paste command to terminal using xdotool after TUI exits."""
        try:
            time.sleep(1)
            # Type the command
            for char in command:
                self.keyboard.press(char)
                self.keyboard.release(char)
                # Add a small delay between key presses for realism (optional)
                time.sleep(0.04)
        except subprocess.CalledProcessError as e:
            print(f"❌ Error pasting command: {e}")
            print(f"💡 Manual copy: {command}")
        except FileNotFoundError:
            print("❌ pynput not found. Please install: pip install pynput")
            print(f"💡 Manual copy: {command}")