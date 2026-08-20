import threading
from time import sleep
from pynput.mouse import Controller as MouseController, Button
from pynput.keyboard import Controller as KeyboardController
from main import run

mouse = MouseController()
keyboard = KeyboardController()

thread = threading.Thread(target=run, daemon=True)
thread.start()

while thread.is_alive():
    print("hi")
