from pydantic import BaseModel
from pynput.keyboard._base import Listener
from typing import Literal, Optional  # pyright: ignore[reportDeprecated]
from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener
from stopwatch import Stopwatch

watch = Stopwatch()
watch.start()


class EventType(BaseModel):
    type: Literal["Key", "MouseButton", "MouseScroll", "MouseMove", "Time"]

class Event(BaseModel):
    type: Literal["Key", "MouseButton", "MouseScroll", "MouseMove", "Time"]
    info: dict = {}
    time: Optional[int | float] = None

events: list[Event] = []

def Log(event: Event):
    events.append(Event(type="Time", time=watch.duration))
    watch.restart()
    events.append(event)


def log_press(event):
    construct = {"key": str(event).split(":")[0].replace("'", "").replace("Key.", ""), "pressStatus": "up"}
    Log(Event(type="Key", info=construct))

def log_release(event):
    construct = {"key": str(event).split(":")[0].replace("'", "").replace("Key.", ""), "pressStatus": "down"}
    Log(Event(type="Key", info=construct))

def log_click(x, y, button, pressed):
    args = locals()
    args["button"] = str(args["button"]).replace("Button.", "")
    Log(Event(info=args, type="MouseButton"))

def log_scroll(x, y, dx, dy):
    args = locals()
    Log(Event(info=args, type="MouseScroll"))

def log_move(x, y):
    args = locals()
    Log(Event(info=args, type="MouseMove"))

keyListen: Listener = KeyboardListener(on_press=log_press, on_release=log_release)
keyListen.start()
mouseListen = MouseListener(on_click=log_click, on_scroll=log_scroll, on_move=log_move)
mouseListen.start()

while len([event for event in events[-20:] if isinstance(event, tuple) and event.type == "Key" and event.info["key"] == "esc"]) != 10:
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

for i in events:
    if i.type == ""