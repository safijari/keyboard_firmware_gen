from helpers import *
from layout import row_pin_map, col_pin_map, layout_left, layout_right, layers
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

    num_keys = 0
    state_idx_to_row_col = {}
    for row_num, cols in layout.items():
        for col_num in cols:
            state_idx_to_row_col[num_keys] = [row_num, col_num]
            num_keys += 1

    row_col_to_state_idx = {rckey(*v): k for k, v in state_idx_to_row_col.items()}

    code += f"""char state[] = {{ {','.join(["'1'"]*num_keys)}"""
    code += """, '\\n'};\n"""

    code += """
void setup() {
    Serial.begin(115200);
    Serial1.begin(115200);
    pinMode(LED_BUILTIN_TX,INPUT);
    pinMode(LED_BUILTIN_RX,INPUT);
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

    for row_num, cols in layout.items():
        code += f"\n  digitalWrite({row(row_num)}, LOW);\n"
        for col_num, _ in cols.items():
            code += f"  check_key_state({col(col_num)}, state[{row_col_to_state_idx[rckey(row_num, col_num)]}]);\n"

        code += f"  digitalWrite({row(row_num)}, HIGH);\n\n"

    code += f"""
    Serial.println(millis());
    """

    code += "\n}"

    return code