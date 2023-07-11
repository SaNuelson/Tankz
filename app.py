import time
import tkinter as tk
from typing import Dict

from config import Config, AppState
from frames.game_play import GamePlay
from frames.game_setup import GameSetup
from frames.menu import Menu
from logic.input import Input


class App(tk.Tk):
    state: AppState = AppState.MENU

    frames: Dict[AppState, tk.Frame]

    def __init__(self):
        super().__init__()
        self.frames = {}

        # set _size, style, font
        geometry_string = str(Config.screen_w) + "x" + str(Config.screen_h)
        self.geometry(geometry_string)
        self.configure(bg=Config.main_bg_color)
        self.option_add("*font", Config.default_font)

        # init frames
        menu = Menu(self)
        menu.pack(fill="both", expand=True)
        self.frames[AppState.MENU] = menu

        game_setup = GameSetup(self)
        game_setup.pack_forget()
        self.frames[AppState.GAME_SETUP] = game_setup

        game_play = GamePlay(self)
        game_play.pack_forget()
        self.frames[AppState.GAME_PLAY] = game_play

        # bind input handler
        Input.bind(self)

        # start custom loop
        self.after(1, self.custom_update)
        self.last_time = time.perf_counter()

    def setState(self, state: AppState):
        if not Config.state_transition(self.state, state):
            return

        if state == AppState.QUIT:
            self.destroy()
            return

        # TODO: temp setup override
        if state == AppState.GAME_SETUP:
            state = AppState.GAME_PLAY

        self.frames[self.state].pack_forget()
        self.frames[state].pack(fill="both", expand=True)
        self.state = state

    def custom_update(self):
        next_time = time.perf_counter()
        self.frames[self.state].custom_update(next_time - self.last_time)
        self.last_time = next_time

        self.after(1, self.custom_update)
