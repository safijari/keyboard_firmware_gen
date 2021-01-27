from helpers import *
from layout import row_pin_map, col_pin_map, layout_left, layout_right, layers
from snippets import preamble, functions

debug = False
nl = '\\n'

def generate_code_primary(layout_primary, layout_secondary, layers):

    code = ""

    code += preamble + "\n"

    code += f"#define DEBUG {int(debug)}\n"

    for row_num, pin in row_pin_map.items():
        code += f"#define {row(row_num)} {pin}\n"

    for col_num, pin in col_pin_map.items():
        code += f"#define {col(col_num)} {pin}\n"

    code += functions + "\n"

    num_keys, row_col_to_state_idx = make_state_map(layout_primary)
    num_keys_sec, row_col_to_state_idx_sec = make_state_map(layout_secondary)

    code += f"""char flags[] = {{ {','.join(["'0'"]*num_keys)} }};\n"""
    code += f"""char flags_sec[] = {{ {','.join(["'0'"]*num_keys)} }};\n"""
    code += f"""KeyTracker trackers[{num_keys}];\n"""
    code += f"""KeyTracker trackers_sec[{num_keys}];\n"""
    code += f"""char state_sec[{num_keys}];\n"""
    code += f"""char state[{num_keys}];\n"""

    code += """
void setup() {
    Serial1.begin(115200);
    Serial.begin(115200);
    pinMode(LED_BUILTIN_TX,INPUT);
    pinMode(LED_BUILTIN_RX,INPUT);
    \n"""

    lnames = list(layers.keys())

    def sanitize_mapped_key(mapped_key):
        if mapped_key in lnames or "LAYER" in mapped_key or "NO_OP" in mapped_key:
            return
        if mapped_key in ["\'", "\\"]:
            mapped_key = "\\" + mapped_key
            mapped_key = f"'{mapped_key}'"

        if len(mapped_key) == 1:
            mapped_key = f"'{mapped_key}'"

        return mapped_key


    for tracker_name, layout in zip(["trackers", "trackers_sec"], [layout_primary, layout_secondary]):
        for row_num, cols in layout_primary.items():
            for col_num, mapped_key in cols.items():
                key = sanitize_mapped_key(mapped_key);
                dont_emit = "true" if not key else "false"
                key = key or "' '"
                code += f"""{tracker_name}[{row_col_to_state_idx[rckey(row_num, col_num)]}] = KeyTracker({key}, {key}, {dont_emit}); \n"""

    for row_num in row_pin_map:
        code += f"  setup_output({row(row_num)});\n"

    for col_num in col_pin_map:
        code += f"  setup_input({col(col_num)});\n"

    code += "  Keyboard.begin();\n delay(1300);\n}"

    code += """\nvoid loop() {
    bool process_seconday = false;
    char to_check;
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

    for row_num, cols in layout_primary.items():
        code += f"\n  digitalWrite({row(row_num)}, LOW);\n"
        for col_num, mapped_key in cols.items():
            code += f"  state[{row_col_to_state_idx_sec[rckey(row_num, col_num)]}] = check_col_down({col(col_num)});\n"
        code += f"  digitalWrite({row(row_num)}, HIGH);\n\n"



    for ln in lnames:
        code += f"int layer_{ln}_down = 0;\n"
        half = layers[ln]["key"]["half"]
        r, c = layers[ln]["key"]["key"]
        if half == "right":
            code += f"""
    if (check_key_down({col_pin_map[c]}, {row_pin_map[r]})) {{
        layer_{ln}_down = 1;
    }}
            """
        else:
            code += f"""
    if (state_sec[{row_col_to_state_idx_sec[rckey(r, c)]}] == '1') {{
        layer_{ln}_down = 1;
    }}
            \n"""

    for layout, map_name, state_name, tracker_name in zip([layout_primary, layout_secondary], ["map_right", "map_left"], ["state", "state_sec"], ["trackers", "trackers_sec"]):
        for row_num, cols in layout.items():
            for col_num, mapped_key in cols.items():
                idx = f"{row_col_to_state_idx[rckey(row_num, col_num)]}"
                code += f"{tracker_name}[{idx}].update({state_name}[{idx}] == '1');\n"

    code += "\n}"

    return code