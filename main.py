from typing import Literal
from pynput.keyboard import Listener
from stopwatch import Stopwatch

events: list[tuple | float] = []
watch = Stopwatch()
watch.start()


def keyLog(event, type: Literal["up", "down"]):
    print(events)
    events.append(watch.duration)
    watch.restart()
    events.append((str(event).split(":")[0].replace("'", ""), type))

def log_press(event):
    keyLog(event, "down")

def log_release(event):
     keyLog(event, "up")


keyListen = Listener(on_press=log_press, on_release=log_release)
keyListen.start()
keyListen.join()