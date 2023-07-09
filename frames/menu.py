import tkinter as tk

import utils
from components.ImageButton import ImageButton
from config import Config, AppState


class Menu(tk.Frame):
    def __init__(self, master):
        super().__init__(master, width=Config.screen_w, height=Config.screen_h)
        self.configure(bg=Config.main_bg_color)

        image_width = min(600, Config.screen_w - 2 * Config.screen_pad_x)
        image = utils.load_photo(Config.res_path_logo, width=image_width)
        self.banner_canvas = tk.Canvas(self, width=image_width, height=image.height(),
                                       bd=0, highlightthickness=0, relief='ridge')
        self.banner_canvas.pack(padx=Config.screen_pad_x, pady=Config.screen_pad_y)
        self.banner_canvas.create_image(0, 0, image=image, anchor="nw")
        self.banner_canvas.configure(bg=Config.main_bg_color)

        self.startBtn = ImageButton.PackDefault(self, "Start", width=Config.button_w, command=self.onStart)
        self.startBtn.pack(pady=(Config.screen_pad_y, 0))

        self.quitBtn = ImageButton.PackDefault(self, "Quit", width=Config.button_w, command=self.onQuit)
        self.quitBtn.pack(pady=(Config.screen_pad_y, 0))

    def onStart(self):
        self.master.setState(AppState.GAME_SETUP)

    def onQuit(self):
        self.master.setState(AppState.QUIT)

    def custom_update(self, delta: float):
        return