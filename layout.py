row_pin_map = {
    1: 9,
    2: 8,
    3: 7,
    4: 6,
    5: 5,
    6: 4,
    7: 3,
    8: 2,
}

col_pin_map = {
    1: 10,
    2: 16,
    3: 14,
    4: 15,
    5: "A0",
    6: "A1",
}

"""
Available inputs are:
a-z (lowercase)
0-9
everything at http://www.asciitable.com/
KEY_LEFT_CTRL
KEY_LEFT_SHIFT
KEY_LEFT_ALT
KEY_LEFT_GUI
KEY_RIGHT_CTRL
KEY_RIGHT_SHIFT
KEY_RIGHT_ALT
KEY_RIGHT_GUI
KEY_UP_ARROW
KEY_DOWN_ARROW
KEY_LEFT_ARROW
KEY_RIGHT_ARROW
KEY_BACKSPACE
KEY_TAB
KEY_RETURN
KEY_ESC
KEY_INSERT
KEY_DELETE
KEY_PAGE_UP
KEY_PAGE_DOWN
KEY_HOME
KEY_END
KEY_CAPS_LOCK
KEY_F1
KEY_F2
KEY_F3
KEY_F4
KEY_F5
KEY_F6
KEY_F7
KEY_F8
KEY_F9
KEY_F10
KEY_F11
KEY_F12
KEY_F13
KEY_F14
KEY_F15
KEY_F16
KEY_F17
KEY_F18
KEY_F19
KEY_F20
KEY_F21
KEY_F22
KEY_F23
KEY_F24
"""

layout_left = {
    1: {1: "NO_OP", 2: "NO_OP", 3: "NO_OP", 4: "NO_OP", 5: "NO_OP", 6: "NO_OP",},
    2: {1: "=", 2: "q", 3: "w", 4: "e", 5: "r", 6: "t",},
    3: {1: ["KEY_LEFT_GUI", "KEY_TAB"], 2: "a", 3: "s", 4: "d", 5: "f", 6: "g",},
    4: {1: "KEY_LEFT_SHIFT", 2: "z", 3: "x", 4: "c", 5: "v", 6: "b",},
    5: {1: "LAYER", 2: "`", 3: "MOUSE_MIDDLE", 4: "MOUSE_LEFT", 5: "MOUSE_RIGHT",},
    6: {5: "KEY_BACKSPACE", 6: "KEY_LEFT_CTRL",},
    7: {5: "LAYER", 6: "LAYER",},
    8: {5: "KEY_ESC", 6: "KEY_LEFT_ALT",},
}

layout_right = {
    1: {1: "NO_OP", 2: "NO_OP", 3: "NO_OP", 4: "NO_OP", 5: "NO_OP", 6: "NO_OP",},
    2: {1: ["LAYER", "\\"], 2: "p", 3: "o", 4: "i", 5: "u", 6: "y",},
    3: {1: "'", 2: ";", 3: "l", 4: "k", 5: "j", 6: "h",},
    4: {1: "KEY_RIGHT_SHIFT", 2: "/", 3: ".", 4: ",", 5: "m", 6: "n",},
    5: {1: "LAYER", 2: "]", 3: "[", 4: "NO_OP", 5: "NO_OP",},
    6: {5: " ", 6: "KEY_RIGHT_CTRL",},
    7: {5: "LAYER", 6: "KEY_RIGHT_GUI",},
    8: {5: "KEY_RETURN", 6: "KEY_RIGHT_ALT",},
}

layers = {
    "nav": {
        "key": {"half": "left", "key": [7, 5], "hold": True},
        "map_right": {
            2: {
                2: "_",
                3: "KEY_END",
                6: "KEY_HOME",
                4: "KEY_PAGE_UP",
                5: "KEY_PAGE_DOWN",
            },
            3: {
                2: "-",
                6: "KEY_LEFT_ARROW",
                5: "KEY_DOWN_ARROW",
                4: "KEY_UP_ARROW",
                3: "KEY_RIGHT_ARROW",
            },
            4: {
                6: {"device": "CTRL", "code": "KEY_LEFT_ARROW"},
                3: {"device": "CTRL", "code": "KEY_RIGHT_ARROW"},
                5: {"device": "WHEEL", "code": "WHEEL_DOWN"},
                4: {"device": "WHEEL", "code": "WHEEL_UP"},
            },
            5: {
                5: {"device": "ALT", "code": "KEY_LEFT_ARROW"},
                4: {"device": "ALT", "code": "KEY_RIGHT_ARROW"},
            },
        },
        "map_left": {
            # 4: {3: "1", 4: "2", 5: "3", 6: "0"},
            # 3: {3: "4", 4: "5", 5: "6", 6: "."},
            # 2: {3: "7", 4: "8", 5: "9"},
        },
    },
    "symbols": {
        "key": {"half": "right", "key": [7, 5], "hold": True},
        "map_right": {2: {1: "_", 2: ")", 3: "(", 4: "*", 5: "&", 6: "^"},
                      3: {6: "6", 5: "7", 4: "8", 3: "9", 2: "0", 1: "-"}},
        "map_left": {
            2: {1: "`", 2: "!", 3: "@", 4: "#", 5: "$", 6: "%"},
            3: {2: "1", 3: "2", 4: "3", 5: "4", 6: "5"},
            6: {5: {"device": "ALT", "code": "KEY_BACKSPACE"}}
        },
    },
    "fn": {
        "key": {"half": "right", "key": [5, 1], "hold": True},
        "map_left": {
            1: {
                1: "KEY_F11",
                2: "KEY_F1",
                3: "KEY_F2",
                4: "KEY_F3",
                5: "KEY_F4",
                6: "KEY_F5",
            },
        },
        "map_right": {
            1: {
                1: "KEY_F12",
                2: "KEY_F10",
                3: "KEY_F9",
                4: "KEY_F8",
                5: "KEY_F7",
                6: "KEY_F6",
            },
        },
    },
    "i3": {
        "key": {"half": "right", "key": [2, 1], "hold": True},
        "device_override": "SUPER_SHIFT",
        "map_left": {},
        "map_right": {},
    },
    # "TMUX": {
    #     "key": {"half": "left", "key": [8, 5], "hold": True},
    #     "device_override": "CTRL_B",
    #     "map_right": {},
    #     "map_left": {},
    # },
}
