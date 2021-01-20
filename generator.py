from layout import row_pin_map, col_pin_map, layout_left, layout_right, layers_right, layers_left
from snippets import preamble, functions
from seconday import generate_code_secondary
from primary import generate_code_primary
from helpers import *

debug = False

def generate_code(layout, layers):

    code = ""

    code += preamble + "\n"

    code += f"#define DEBUG {int(debug)}\n"

    for row_num, pin in row_pin_map.items():
        code += f"#define {row(row_num)} {pin}\n"

    for col_num, pin in col_pin_map.items():
        code += f"#define {col(col_num)} {pin}\n"

    code += functions + "\n"

    for row_num, cols in layout.items():
        for col_num in cols:
            code += f"int {down(row_num, col_num)} = 0;\n"

    code += """
void setup() {
    \n"""

    for row_num in row_pin_map:
        code += f"  setup_output({row(row_num)});\n"

    for col_num in col_pin_map:
        code += f"  setup_input({col(col_num)});\n"

    code += "  Keyboard.begin();\n delay(300);\n}"

    code += """\nvoid loop() {
    char to_check;
    """

    lnames = list(layers.keys())

    for ln in lnames:
        code += f"int layer_{ln}_down = 0;\n"
        r, c = layers[ln]["key"]
        code += f"""
    if (check_key_down({row_pin_map[r]}, {col_pin_map[c]})) {{
        layer_{ln}_down = 1;
    }}
        """

    for row_num, cols in layout.items():
        code += f"\n  digitalWrite({row(row_num)}, LOW);\n"
        for col_num, mapped_key in cols.items():
            is_mouse = "false"
            if mapped_key in ["\'", "\\"]:
                mapped_key = "\\" + mapped_key
                mapped_key = f"'{mapped_key}'"

            if len(mapped_key) == 1:
                mapped_key = f"'{mapped_key}'"
            code += f"  to_check = {mapped_key};\n"
            for ln in lnames:
                new_key = layers[ln].get(row_num, {}).get(col_num, None)
                if not new_key:
                    continue
                code += f"  if (layer_{ln}_down == 1) {{to_check = {new_key};}}\n"
            if "MOUSE" in mapped_key:
                is_mouse = "true"
            code += f"  check_key({col(col_num)}, {down(row_num, col_num)}, to_check, {row_num}, {col_num}, {is_mouse});\n\n"

        code += f"  digitalWrite({row(row_num)}, HIGH);\n\n"

    code += """
    """

    code += "\n}"

    return code


# if __name__ == "__main__":
#     with open("/mnt/c/Users/janso/OneDrive/Desktop/dactyl_left/dactyl_left.ino", "w") as ff:
#         ff.write(generate_code(layout_left, layers_left))

#     with open("/mnt/c/Users/janso/OneDrive/Desktop/dactyl_right/dactyl_right.ino", "w") as ff:
#         ff.write(generate_code(layout_right, layers_right))

# with open("/mnt/c/Users/janso/OneDrive/Desktop/dactyl_left/dactyl_left.ino", "w") as ff:
#     ff.write(generate_code_secondary(layout_left))

# with open("/mnt/c/Users/janso/OneDrive/Desktop/dactyl_right/dactyl_right.ino", "w") as ff:
#     ff.write(generate_code_primary(layout_right, layout_left, layers_right))

if __name__ == "__main__":
    with open("/tmp/dactyl_left/dactyl_left.ino", "w") as ff:
        ff.write(generate_code(layout_left, layers_left))

    with open("/tmp/dactyl_right.ino", "w") as ff:
        ff.write(generate_code(layout_right, layers_right))