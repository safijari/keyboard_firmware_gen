from layout import row_pin_map, col_pin_map, layout_left, layout_right, layers
from snippets import preamble, functions
from seconday import generate_code_secondary
from primary import generate_code_primary
from helpers import *
import os

if __name__ == "__main__":
    try:
        os.makedirs("/tmp/dactyl_left/")
    except Exception:
        pass

    with open("/tmp/dactyl_left/dactyl_left.ino", "w") as ff:
        ff.write(generate_code_secondary(layout_left))

    try:
        os.makedirs("/tmp/dactyl_right/")
    except Exception:
        pass

    with open("/tmp/dactyl_right/dactyl_right.ino", "w") as ff:
        ff.write(generate_code_primary(layout_right, layout_left, layers))
    # with open("/tmp/dactyl_right/dactyl_right.ino", "w") as ff:
    #     ff.write(generate_code(layout_right, layers_right))
