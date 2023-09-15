import time
import tkinter as tk

import toolkit.canvas
from config import Config
from game_components.renderer import SpriteRenderer
from logic.input import Input
from toolkit.vector import Vector2, PartialVector2


class App(tk.Tk):
    last_time: float

    def __init__(self, w=750, h=750):
        super().__init__()
        self.geometry(str(w) + "x" + str(h))

        # bind input handler
        Input.bind(self)

        self.w = w
        self.h = h
        self.canvas = tk.Canvas(self, width=w, height=h, bg="cyan")
        self.canvas.pack()

        margin = Vector2(1, 1) * 75
        offset = Vector2(1, 1) * 150

        self.sprites = [
            SpriteRenderer(self.canvas,
                           '../' + Config.res_path_icon,
                           position=Vector2(x, y) * offset + margin,
                           size=PartialVector2(100, None),
                           anchor=Vector2(0.25 * x, 0.25 * y))
            for x in range(5)
            for y in range(5)
        ]

        diag = self.sprites[0].size
        self.gizmos = \
            [
                toolkit.canvas.draw_x(self.canvas,
                                      Vector2(x, y) * offset + margin, 10,
                                      "red")
                for x in range(5)
                for y in range(5)
            ] + [
                toolkit.canvas.draw_box(self.canvas,
                                        Vector2(x, y) * offset + margin - Vector2(diag.x * x / 4, diag.y * y / 4),
                                        diag, "blue")
                for x in range(5)
                for y in range(5)
            ]
        self.gizmos = [i for s in self.gizmos for i in s]

        # start custom loop
        self.after(1, self.custom_update)
        time.perf_counter()

    def custom_update(self):
        delta = time.perf_counter()
        for sprite in self.sprites:
            sprite.rotation += 0.5
            sprite.custom_update(delta)

        for debug in self.gizmos:
            self.canvas.tag_raise(debug)

        self.after(1, self.custom_update)


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
