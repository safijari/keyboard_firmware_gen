from helpers import *
from layout import row_pin_map, col_pin_map, layout_left, layout_right, layers
from snippets import preamble, functions

debug = False
nl = '\\n'

def generate_code_primary(layout_primary, layout_secondary, layers):

    code = ""

    code += preamble + "\n"

    code += f"#define DEBUG {int(debug)}\n"
    code += f"#define NO_OP 255\n"

    for row_num, pin in row_pin_map.items():
        code += f"#define {row(row_num)} {pin}\n"

    for col_num, pin in col_pin_map.items():
        code += f"#define {col(col_num)} {pin}\n"

    code += functions + "\n"

    num_keys, row_col_to_state_idx, flat_map = make_state_map(layout_primary, "right")
    num_keys_sec, row_col_to_state_idx_sec, flat_map_sec = make_state_map(layout_secondary, "left")

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

    code += f"""char flags[] = {{ {','.join(["'0'"]*num_keys)} }};\n"""
    code += f"""char flags_sec[] = {{ {','.join(["'0'"]*num_keys)} }};\n"""
    code += f"""KeyTracker trackers[{num_keys}];\n"""
    code += f"""KeyTracker trackers_sec[{num_keys}];\n"""
    code += f"""char state_sec[{num_keys}];\n"""
    code += f"""char state[{num_keys}];\n"""

    for ln in ["base"] + lnames:
        code += f"""char {ln}_map[] = {{""" + ", ".join([sanitize_mapped_key(k) or "NO_OP" for k in make_state_map(layout_primary, "right", layers.get(ln, {}))[-1]]) + "};\n"
        code += f"""char {ln}_map_sec[] = {{""" + ", ".join([sanitize_mapped_key(k) or "NO_OP" for k in make_state_map(layout_secondary, "left", layers.get(ln, {}))[-1]]) + "};\n"

    code += """
void setup() {
    Serial1.begin(115200);
    Serial.begin(115200);
    pinMode(LED_BUILTIN_TX,INPUT);
    pinMode(LED_BUILTIN_RX,INPUT);
    \n"""

    # for tracker_name, layout in zip(["trackers", "trackers_sec"], [layout_primary, layout_secondary]):
    #     for row_num, cols in layout_primary.items():
    #         for col_num, mapped_key in cols.items():
    #             key = sanitize_mapped_key(mapped_key);
    #             dont_emit = "true" if not key else "false"
    #             key = key or "' '"
    #             code += f"""{tracker_name}[{row_col_to_state_idx[rckey(row_num, col_num)]}] = KeyTracker({key}, {key}, {dont_emit}); \n"""

    for row_num in row_pin_map:
        code += f"  setup_output({row(row_num)});\n"

    for col_num in col_pin_map:
        code += f"  setup_input({col(col_num)});\n"

    code += "  Keyboard.begin();\n delay(1300);\n}"

    code += """\nvoid loop() {

    auto curr_map = base_map;
    auto curr_map_sec = base_map_sec;

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


    for tracker_name, state_name in zip(["trackers", "trackers_sec"], ["state", "state_sec"]):
        code += f"for (int i = 0; i < {num_keys}; i++) {{" + NL
        code += f"  {tracker_name}[i].update({state_name}[i] == '1');{NL}}}" + NL

    for ln, layer in layers.items():
        half = layer["key"]["half"]
        suffix = "" if half == "right" else "_sec"
        r, c = layer["key"]["key"]
        code += f"""if (trackers{suffix}[{row_col_to_state_idx[rckey(r, c)]}].primary_down()) {{
        curr_map = {ln}_map;
        curr_map_sec = {ln}_map_sec;
}}
"""
    for suffix in ["", "_sec"]:
        code += f"for (int i = 0; i < {num_keys}; i++) {{" + NL
        code += f"  trackers{suffix}[i].emit(curr_map{suffix}[i]);{NL}}}" + NL

    code += "\n}"

    return code