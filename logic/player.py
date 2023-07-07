from config import InputKey
from logic.input import Input
from logic.tank import Tank


class Player:
    def __init__(self, tank: Tank):
        self.tank = tank


    def make_turn(self):
        pass


class Human(Player):
    def __init__(self, tank: Tank):
        super().__init__(tank)

    def make_turn(self):
        Input.key_down[InputKey.DOWN].append(self.tank.aim_minus)
        Input.key_down[InputKey.UP].append(self.tank.aim_plus)
        Input.key_down[InputKey.LEFT].append(self.tank.move_left)
        Input.key_down[InputKey.RIGHT].append(self.tank.move_right)


class NPC(Player):
    def __init__(self, tank: Tank):
        super().__init__(tank)