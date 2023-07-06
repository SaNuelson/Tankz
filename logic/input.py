import tkinter as tk
from typing import Dict

from config import AppState, InputKey, Config
from logic.event import Event


class _Input:
    key_down: Dict[InputKey, Event]

    def __init__(self):
        self.app = None
        self.key_down = {}
        for key in list(InputKey):
            self.key_down[key] = Event()

    def bind(self, app: tk.Misc):
        self.app = app
        app.bind('<KeyPress>', self.on_key_press)

    def on_key_press(self, event: tk.Event):
        for key in list(InputKey):
            if event.keysym in Config.control_keysyms[key]:
                self.key_down[key]()
                return


Input = _Input()
