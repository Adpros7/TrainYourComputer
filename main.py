from pathlib import Path
from pydantic import BaseModel
from pynput.keyboard._base import Listener
from typing import Literal
from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener
from stopwatch import Stopwatch

events: list = []
watch = Stopwatch()
watch.start()


class EventType(BaseModel):
    type: Literal["Key", "MouseButton", "MouseScroll", "MouseMove"]

def Log(event: dict, type: EventType):
    events.append(watch.duration)
    watch.restart()
    events.append((event, type))


def log_press(event):
    construct = {"key": str(event).split(":")[0].replace("'", "").replace("Key.", ""), "pressStatus": "up"}
    Log(construct, EventType(type="Key"))

def log_release(event):
    construct = {"key": str(event).split(":")[0].replace("'", "").replace("Key.", ""), "pressStatus": "down"}
    Log(construct, EventType(type="Key"))

def log_click(x, y, button, pressed):
    args = locals()
    print(args)
    args["button"] = str(args["button"]).replace("Button.", "")
    Log(args, EventType(type="MouseButton"))

def log_scroll(x, y, dx, dy):
    args = locals()
    Log(args, EventType(type="MouseScroll"))

def log_move(x, y):
    args = locals()
    Log(args, EventType(type="MouseMove"))

keyListen: Listener = KeyboardListener(on_press=log_press, on_release=log_release)
keyListen.start()
mouseListen = MouseListener(on_click=log_click, on_scroll=log_scroll, on_move=log_move)
mouseListen.start()

while len([event for event in events[-20:] if isinstance(event, tuple) and event[1].type == "Key" and event[0]["key"] == "esc"]) != 10:
    pass

keyListen.stop()
mouseListen.stop()

print(events)

template = """from time import sleep
from pynput.mouse import Controller as MouseController, Button
from pynput.keyboard import Controller as KeyboardController

mouse = MouseController()
keyboard = KeyboardController()

"""

