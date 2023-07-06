from typing import Callable

from PIL import Image, ImageTk
import tkinter as tk

import utils
from config import Config


class ImageButton(tk.Button):
    def __init__(self, master, image_idle, image_pressed, *args, **kwargs):
        self.unclickedImage = image_idle
        self.clickedImage = image_pressed
        super().__init__(master, *args, image=self.unclickedImage, **kwargs)
        self.toggleState = 1
        self.bind("<Button-1>", self.press_function)
        self.bind("<ButtonRelease-1>", self.release_function)

    def press_function(self, event=None):
        if self.cget("state") != "disabled":
            self.config(image=self.clickedImage)

    def release_function(self, event=None):
        if self.cget("state") != "disabled":
            self.config(image=self.unclickedImage)

    def click_function(self, event=None):
        if self.cget("state") != "disabled":  # Ignore click if button is disabled
            self.toggleState *= -1
            if self.toggleState == -1:
                self.config(image=self.clickedImage)
            else:
                self.config(image=self.unclickedImage)

    @staticmethod
    def PackDefault(master: tk.Misc, text: str, command: Callable, width: int | None = None, height: int | None = None):
        base_image = utils.load_photo(Config.res_path_btn_idle, width=width, height=height)
        down_image = utils.load_photo(Config.res_path_btn_down, width=width, height=height)
        button = ImageButton(master, base_image, down_image,
                             text=text,
                             command=command,
                             compound="center",
                             bd=0,
                             background=Config.main_bg_color,
                             activebackground=Config.main_bg_color)
        return button

    @staticmethod
    def PackArrow(master: tk.Misc, text: str, command: Callable,
                  width: int | None = None, height: int | None = None,
                  rotate: int = 0, flip_h: bool = False, flip_v: bool = False,
                  red: bool = False):
        idle_path = Config.res_path_red_arrow_idle if red else Config.res_path_green_arrow_idle
        down_path = Config.res_path_red_arrow_down if red else Config.res_path_green_arrow_down
        base_image = utils.load_photo(idle_path, width=width, height=height, rotate=rotate, flip_v=flip_v,
                                      flip_h=flip_h)
        down_image = utils.load_photo(down_path, width=width, height=height, rotate=rotate, flip_v=flip_v,
                                      flip_h=flip_h)
        button = ImageButton(master, base_image, down_image,
                             text=text,
                             command=command,
                             compound="center",
                             bd=0,
                             background=Config.main_bg_color,
                             activebackground=Config.main_bg_color)
        return button

    @staticmethod
    def PackArrowGreenRight(master: tk.Misc, text: str, command: Callable):
        return ImageButton.PackArrow(master, text, command, Config.arrow_w)

    @staticmethod
    def PackArrowGreenLeft(master: tk.Misc, text: str, command: Callable):
        return ImageButton.PackArrow(master, text, command, Config.arrow_w, flip_h=True)

    @staticmethod
    def PackArrowRedRight(master: tk.Misc, text: str, command: Callable):
        return ImageButton.PackArrow(master, text, command, Config.arrow_w, red=True)

    @staticmethod
    def PackArrowRedLeft(master: tk.Misc, text: str, command: Callable):
        return ImageButton.PackArrow(master, text, command, Config.arrow_w, red=True, flip_h=True)


