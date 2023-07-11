from __future__ import annotations

from typing import TYPE_CHECKING

from config import InputKey
from logic.input import Input
from logic.tank import Tank

if TYPE_CHECKING:
    from frames.game_play import GamePlay


class Player:
    def __init__(self, game: GamePlay, tank: Tank):
        self.game = game
        self.tank = tank

    def custom_update(self, delta: float):
        self.tank.custom_update(delta)

    def start_turn(self):
        pass


class Human(Player):

    connected: bool = False

    def start_turn(self):
        if not self.connected:
            print("Player input connected")
            Input.key_down[InputKey.DOWN].append(self.tank.aim_minus)
            Input.key_down[InputKey.UP].append(self.tank.aim_plus)
            Input.key_down[InputKey.LEFT].append(self.tank.move_left)
            Input.key_down[InputKey.RIGHT].append(self.tank.move_right)
            Input.key_down[InputKey.SELECT].append(self.tank.fire)
            self.connected = True

    def end_turn(self):
        if self.connected:
            print("Player input disconnected")
            Input.key_down[InputKey.DOWN].remove(self.tank.aim_minus)
            Input.key_down[InputKey.UP].remove(self.tank.aim_plus)
            Input.key_down[InputKey.LEFT].remove(self.tank.move_left)
            Input.key_down[InputKey.RIGHT].remove(self.tank.move_right)
            Input.key_down[InputKey.SELECT].remove(self.tank.fire)
            self.connected = False


class NPC(Player):
    pass
