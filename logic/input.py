import tkinter as tk
from typing import Dict

from config import AppState, InputKey, Config
from logic.event import Event


class _Input:
    key_down: Dict[InputKey, Event]

    debug: bool = False

    def __init__(self):
        self.app = None
        self.key_down = {}
        i=0
        for key in list(InputKey):
            self.key_down[key] = Event()
            if self.debug:
                self.key_down[key].append(lambda key=key: print("Pressed", key))

    def bind(self, app: tk.Misc):
        self.app = app
        app.bind('<KeyPress>', self.on_key_press)
        pass

    def on_key_press(self, event: tk.Event):
        for key in list(InputKey):
            if event.keysym in Config.control_keysyms[key]:
                self.key_down[key]()
                return


Input = _Input()
