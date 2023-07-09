from enum import Enum, IntEnum


class String(Enum):
    Start = 1
    Exit = 2
    NoOfPlayers = 3


class AppState(IntEnum):
    MENU = 1
    SETTINGS = 2
    GAME_SETUP = 3
    GAME_PLAY = 4
    QUIT = 5


class InputKey(Enum):
    UP = 'Up'
    DOWN = 'Down'
    LEFT = 'Left'
    RIGHT = 'Right'


class Config:
    screen_w = 800
    screen_h = 600

    screen_pad_x = 20
    screen_pad_y = 20

    button_w = 200
    arrow_w = 80

    tank_w = 50
    cannon_w = 25
    cannon_offset = (8, -10)

    main_bg_color = "green"

    default_font = "lucida 20 bold italic"

    res_path_logo = "./res/logo.png"
    res_path_btn_idle = "./res/btn.png"
    res_path_btn_down = "./res/btn_down.png"
    res_path_green_arrow_idle = "./res/arrow.png"
    res_path_green_arrow_down = "./res/arrow_down.png"
    res_path_red_arrow_idle = "./res/arrow_red.png"
    res_path_red_arrow_down = "./res/arrow_red_down.png"
    res_path_tank_base = "./res/tank_base.png"
    res_path_tank_cannon = "./res/tank_cannon.png"
    res_path_skytex = "./res/skytex.png"

    min_player_count = 2
    max_player_count = 8

    rgba_earth_top = [74, 86, 106, 255]
    rgba_earth_bot = [41, 47, 56, 255]

    phys_gravity = (0, 9.8)

    control_keysyms = {
        InputKey.UP: ['w', 'W', 'Up'],
        InputKey.DOWN: ['s', 'S', 'Down'],
        InputKey.LEFT: ['a', 'A', 'Left'],
        InputKey.RIGHT: ['d', 'D', 'Right']
    }

    __state_transitions_matrix = [
        [1, 1, 1, 0, 1],
        [1, 1, 0, 0, 0],
        [1, 0, 1, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0]
    ]

    @staticmethod
    def state_transition(old_state, new_state):
        return Config.__state_transitions_matrix[old_state - 1][new_state - 1]

    locale = "en"

    __lang_strings = {
        "en": {
            String.Start: "Start",
            String.Exit: "Exit",
            String.NoOfPlayers: "Number of players"
        },
        "sk": {
            String.Start: "Spustiť",
            String.Exit: "Ukončiť",
            String.NoOfPlayers: "Počet hráčov"
        }
    }

    @staticmethod
    def string(string: String, lang: str | None = None):
        if lang is None:
            lang = Config.locale
        if lang not in Config.__lang_strings:
            lang = "en"
        return Config.__lang_strings[Config.locale][string]
