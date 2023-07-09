from config import InputKey
from logic.input import Input
from logic.tank import Tank


class Player:
    def __init__(self, tank: Tank):
        self.tank = tank

    def custom_update(self, delta: float):
        self.tank.custom_update(delta)

    def start_turn(self):
        pass


class Human(Player):

    connected: bool = False

    def __init__(self, tank: Tank):
        super().__init__(tank)

    def start_turn(self):
        if not self.connected:
            print("Player input connected")
            Input.key_down[InputKey.DOWN].append(self.tank.aim_minus)
            Input.key_down[InputKey.UP].append(self.tank.aim_plus)
            Input.key_down[InputKey.LEFT].append(self.tank.move_left)
            Input.key_down[InputKey.RIGHT].append(self.tank.move_right)
            self.connected = True

    def end_turn(self):
        if self.connected:
            print("Player input disconnected")
            Input.key_down[InputKey.DOWN].remove(self.tank.aim_minus)
            Input.key_down[InputKey.UP].remove(self.tank.aim_plus)
            Input.key_down[InputKey.LEFT].remove(self.tank.move_left)
            Input.key_down[InputKey.RIGHT].remove(self.tank.move_right)
            self.connected = False


class NPC(Player):
    def __init__(self, tank: Tank):
        super().__init__(tank)