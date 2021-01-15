from helpers import *
from layout import row_pin_map, col_pin_map, layout_left, layout_right, layers_right, layers_left
from snippets import preamble, functions

debug = False

def generate_code_secondary(layout):
    code = ""
    code += preamble + "\n"
    code += f"#define DEBUG {int(debug)}\n"

    for row_num, pin in row_pin_map.items():
        code += f"#define {row(row_num)} {pin}\n"

    for col_num, pin in col_pin_map.items():
        code += f"#define {col(col_num)} {pin}\n"

    code += functions + "\n"

    num_keys, row_col_to_state_idx = make_state_map(layout)

    code += f"""char state[] = {{ {','.join(["'0'"]*num_keys)}"""
    code += """, '\\n'};\n"""

    code += """
void setup() {
    Serial.begin(115200);
    Serial1.begin(115200);
    \n"""

    for row_num in row_pin_map:
        code += f"  setup_output({row(row_num)});\n"

    for col_num in col_pin_map:
        code += f"  setup_input({col(col_num)});\n"

    code += "  Keyboard.begin();\n delay(1300);\n}"

    code += f"""
    void loop() {{
    Serial1.write(state, {num_keys + 1});
    Serial.write(state, {num_keys + 1});
    """

    code += f"""
    Serial.println(millis());
    """

    code += "\n}"

    return code