row_pin_map = {
    1: 9,
    2: 8,
    3: 7,
    4: 6,
    5: 5,
    6: 3
}

col_pin_map = {
    1: 10,
    2: 16,
    3: 14,
    4: 15,
    5: "A0",
    6: "A1",
    7: "A2"
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

layout = {
    1: {
        1: "`",
        2: "=",
        3: "-",
        4: "0",
        5: "9",
        6: "8",
        7: "7",
        },
    2: {
        1: "\\",
        2: "p",
        3: 'o',
        4: 'i',
        5: 'u',
        6: 'y',
        7: ']',
    },
    3: {
        1: "KEY_RIGHT_SHIFT",
        2: "'",
        3: 'l',
        4: 'k',
        5: 'j',
        6: 'h',
        #7: 'h',
    },
    4: {
        2: "/",
        3: '.',
        4: ',',
        5: 'm',
        6: 'n',
    },
    5: {
        2: "KEY_ESC",
        3: "KEY_UP_ARROW",
        4: "KEY_DOWN_ARROW",
        5: ' ',
        6: 'KEY_RETURN',
    },
    6: {
        2: "KEY_RIGHT_ALT",
    },
}