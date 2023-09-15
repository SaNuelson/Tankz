from enum import Enum, IntEnum

from toolkit.vector import Vector2


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
    SELECT = 'Select'
    DEBUG = 'Debug'


class Color(Enum):
    RED = "#ed2543"
    GREEN = "#1adf3f"
    BLUE = "#402ae5"
    CYAN = "#2ecca9"
    MAGENTA = "#cc2a49"
    MAGENTA_LIGHT = "#cc82ab"


class Config:
    debug_mode = False

    screen_w = 800
    screen_h = 600

    screen_pad_x = 20
    screen_pad_y = 20

    button_w = 200
    arrow_w = 80

    tank_w = 50
    cannon_w = 25
    ball_w = 10
    cannon_offset = (8, -10)

    main_bg_color = "green"

    default_font = "lucida 20 bold italic"

    res_path_icon = "./res/icon.png"
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
    res_path_ball = "./res/ball.png"
    res_path_fire_particle = "./res/fire_particle.png"

    min_player_count = 2
    max_player_count = 8

    rgba_earth_top = [74, 86, 106, 255]
    rgba_earth_bot = [41, 47, 56, 255]

    pixels_per_meter = 8.0
    phys_gravity = Vector2(0, 9.8)
    air_density = 1.293  # kg/m^3
    cannonball_k = 0.00001

    gizmo_color_primary = Color.MAGENTA.value
    gizmo_color_secondary = Color.MAGENTA_LIGHT.value

    control_keysyms = {
        InputKey.UP: ['w', 'W', 'Up'],
        InputKey.DOWN: ['s', 'S', 'Down'],
        InputKey.LEFT: ['a', 'A', 'Left'],
        InputKey.RIGHT: ['d', 'D', 'Right'],
        InputKey.SELECT: ['space', 'Enter', 'Return'],
        InputKey.DEBUG: ['f3', 'F3']
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

