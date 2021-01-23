from helpers import *
from layout import row_pin_map, col_pin_map, layout_left, layout_right, layers
from snippets import preamble, functions

debug = False
nl = '\\n'

def generate_code_primary(layout, layout_secondary, layers):

    code = ""

    code += preamble + "\n"

    code += f"#define DEBUG {int(debug)}\n"

    for row_num, pin in row_pin_map.items():
        code += f"#define {row(row_num)} {pin}\n"

    for col_num, pin in col_pin_map.items():
        code += f"#define {col(col_num)} {pin}\n"

    code += functions + "\n"

    num_keys, row_col_to_state_idx = make_state_map(layout)
    num_keys_sec, row_col_to_state_idx_sec = make_state_map(layout_secondary)

    code += f"""char flags[] = {{ {','.join(["'0'"]*num_keys)} }};\n"""
    code += """char state_sec[100];\n"""
    code += f"""char flags_sec[] = {{ {','.join(["'0'"]*num_keys)} }};\n"""

    code += """
void setup() {
    Serial1.begin(115200);
    Serial.begin(115200);
    \n"""

    for row_num in row_pin_map:
        code += f"  setup_output({row(row_num)});\n"

    for col_num in col_pin_map:
        code += f"  setup_input({col(col_num)});\n"

    code += "  Keyboard.begin();\n delay(1300);\n}"

    code += """\nvoid loop() {
    bool process_seconday = false;
    char to_check;
    char key_state = '0';
    bool is_mouse = false;
    Serial.println(millis());
    """

    code += f"""
    if (Serial1.available()) {{
        int tots = Serial1.readBytesUntil('{nl}', state_sec, {num_keys_sec} + 10);
        if (tots == {num_keys_sec}) {{
            Serial.println(tots);
            Serial.write(state_sec, tots);
            Serial.println();
            process_seconday = true;
        }}
        else {{
            // Serial.println("miss");
        }}
    }}
    """


    lnames = list(layers.keys())

    for ln in lnames:
        code += f"int layer_{ln}_down = 0;\n"
        half = layers[ln]["key"]["half"]
        r, c = layers[ln]["key"]["key"]
        if half == "right":
            code += f"""
    if (check_key_down({row_pin_map[r]}, {col_pin_map[c]})) {{
        layer_{ln}_down = 1;
    }}
            """
        else:
            code += f"""
    if (state_sec[{row_col_to_state_idx_sec[rckey(r, c)]}] == '1') {{
        layer_{ln}_down = 1;
    }}
            """

    def sanitize_mapped_key(mapped_key):
        if mapped_key in lnames or "LAYER" in mapped_key or "NO_OP" in mapped_key:
            return
        if mapped_key in ["\'", "\\"]:
            mapped_key = "\\" + mapped_key
            mapped_key = f"'{mapped_key}'"

        if len(mapped_key) == 1:
            mapped_key = f"'{mapped_key}'"

        return mapped_key

    for row_num, cols in layout.items():
        code += f"\n  digitalWrite({row(row_num)}, LOW);\n"
        for col_num, mapped_key in cols.items():
            is_mouse = "false"
            if "MOUSE" in mapped_key:
                is_mouse = "true"
            mapped_key = sanitize_mapped_key(mapped_key)
            if not mapped_key:
                continue
            code += f"  to_check = {mapped_key};\n"
            code += f"  is_mouse = {is_mouse};\n"
            for ln in lnames:
                new_key = layers[ln]["map_right"].get(row_num, {}).get(col_num, None)
                if not new_key:
                    continue
                code += f"  if (layer_{ln}_down == 1) {{to_check = {new_key};}}\n"
            code += f"  key_state = check_key_down({col(col_num)})? '1' : '0';\n"
            code += f"  hold_key(key_state, flags[{row_col_to_state_idx[rckey(row_num, col_num)]}], to_check, is_mouse);\n\n"

        code += f"  digitalWrite({row(row_num)}, HIGH);\n\n"

    for row_num, cols in layout_secondary.items():
        for col_num, mapped_key in cols.items():
            is_mouse = "false"
            if "MOUSE" in mapped_key:
                is_mouse = "true"
            mapped_key = sanitize_mapped_key(mapped_key)
            if not mapped_key:
                continue
            code += f"  to_check = {mapped_key};\n"
            code += f"  is_mouse = {is_mouse};\n"
            for ln in lnames:
                new_key = layers[ln]["map_left"].get(row_num, {}).get(col_num, None)
                if not new_key:
                    continue
                code += f"  if (layer_{ln}_down == 1) {{to_check = {new_key};}}\n"
            idx = row_col_to_state_idx_sec[rckey(row_num, col_num)]
            code += f"  hold_key(state_sec[{idx}], flags_sec[{idx}], to_check, is_mouse);\n\n"

    code += "\n}"

    return code