import tkinter as tk
from typing import Dict

from config import InputKey, Config
from toolkit.event import Event


class _Input:
    key_down: Dict[InputKey, Event]

    debug: bool = False

    def __init__(self):
        self.app = None
        self.key_down = {}
        for key in list(InputKey):
            self.key_down[key] = Event()
            if self.debug:
                self.key_down[key].append(lambda k=key: print("Pressed", k))

        def toggle_debug():
            Config.debug_mode = not Config.debug_mode
            print("Debug mode turned", "ON" if Config.debug_mode else "OFF")

        self.key_down[InputKey.DEBUG].append(toggle_debug)

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
