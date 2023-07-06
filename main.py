import numpy as np

import utils
from utils import as_image, as_photo
from app import App

import tkinter as tk

def main():
    win = tk.Tk()
    win.geometry("400x400")
    can = tk.Canvas(win, width=400, height=400)
    can.create_image(0, 0, image=as_photo(np.random.uniform(0, 255, (100, 100)).astype(np.uint8)))
    can.pack()
    win.mainloop()
    return

    tankz = App()
    tankz.mainloop()


if __name__ == "__main__":
    main()
