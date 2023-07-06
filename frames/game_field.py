import tkinter as tk
from Tankz import generator as gen
from Tankz import canvas_utils as cu


class Game(tk.Tk):

    def __init__(self, w, h):
        super().__init__()

        # banner_canvas image handle to stop garbage collection
        self.img = None
        self.w = w
        self.h = h

        self.canvas = tk.Canvas(self, width=w, height=h)
        self.canvas.pack()

        self.reset_btn = tk.Button(master=self, text="Reset", command=self.start_map)
        self.reset_btn.pack()

        self.start_map()

    def start_map(self):
        self.img = create_map(self.canvas, self.w, self.h)


def create_map(canvas: tk.Canvas, width: int, height: int) -> tk.PhotoImage:
    # field_arr = random_walk_map(width, height, start_y=3*height//4, step_func=random_step_func)
    field_arr = gen.wave_sum_map(width, height)
    field_img = cu.as_photo(field_arr)
    canvas.create_image(0, 0, image=field_img, anchor=tk.NW)
    return field_img

