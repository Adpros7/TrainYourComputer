from pynput.keyboard._base import Listener
from typing import Literal
from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener
from stopwatch import Stopwatch

events: list[tuple | float] = []
watch = Stopwatch()
watch.start()


def Log(event, type: Literal["up", "down", "click", "scroll", "move"]):
    events.append(watch.duration)
    watch.restart()
    events.append((str(event).split(":")[0].replace("'", "").replace("Key.", ""), type))

def log_press(event):
    Log(event, "down")

def log_release(event):
    Log(event, type="up")

def log_click(event):
    Log(event, "click")

def log_scroll(event):
    Log(event, "scroll")

def log_move(event):
    Log(event, "move")

keyListen: Listener = KeyboardListener(on_press=log_press, on_release=log_release)
keyListen.start()
mouseListen = MouseListener(on_click=log_click, on_scroll=log_scroll, on_move=log_move)
mouseListen.start()

while len([event for event in events[-20:] if isinstance(event, tuple) and event[0] == "esc"]) != 10:
    pass

keyListen.stop()
mouseListen.stop()

print(events)
