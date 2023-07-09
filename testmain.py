import time
import tkinter as tk

import toolkit.canvas
import utils
from config import Config
from logic.renderer import SpriteRenderer
from logic.vector import Vector2, PartialVector2


class App(tk.Tk):
    last_time: float

    def __init__(self, w=800, h=800):
        super().__init__()
        self.geometry(str(w) + "x" + str(h))

        self.w = w
        self.h = h
        self.canvas = tk.Canvas(self, width=w, height=h, bg="cyan")
        self.canvas.pack()

        self.sprites = [
            SpriteRenderer(self.canvas, Config.res_path_logo, position=Vector2(300, 300), size=PartialVector2(100, None), anchor=Vector2(0, 0)),
            SpriteRenderer(self.canvas, Config.res_path_logo, position=Vector2(300, 500), size=PartialVector2(100, None), anchor=Vector2(1, 0)),
            SpriteRenderer(self.canvas, Config.res_path_logo, position=Vector2(500, 300), size=PartialVector2(100, None), anchor=Vector2(0, 1)),
            SpriteRenderer(self.canvas, Config.res_path_logo, position=Vector2(500, 500), size=PartialVector2(100, None), anchor=Vector2(1, 1))
        ]

        tl = self.sprites[0].size / 2
        tr = Vector2(tl.x, -tl.y)

        self.gizmos = [
            *toolkit.canvas.draw_x(self.canvas, Vector2(300, 300) - tl, 10, "red"),
            *toolkit.canvas.draw_x(self.canvas, Vector2(300, 500) + tr, 10, "red"),
            *toolkit.canvas.draw_x(self.canvas, Vector2(500, 300) - tr, 10, "red"),
            *toolkit.canvas.draw_x(self.canvas, Vector2(500, 500) + tl, 10, "red"),
        ]

        # start custom loop
        self.after(1, self.custom_update)
        time.perf_counter()

    def custom_update(self):
        delta = time.perf_counter()
        for sprite in self.sprites:
            sprite.position += Vector2(1, 0)
            sprite.custom_update(delta)

        for debug in self.gizmos:
            self.canvas.tag_raise(debug)

        self.after(1, self.custom_update)


def main():
    app = App()
    app.mainloop()



if __name__ == "__main__":
    main()
