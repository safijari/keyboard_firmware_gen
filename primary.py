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

    code += f"""KeyTracker trackers[{num_keys}];\n"""
    code += f"""KeyTracker trackers_sec[{num_keys}];\n"""
    code += f"""char state_sec[{num_keys}];\n"""
    code += f"""char state[{num_keys}];\n"""

    def keymap_to_indkeymap(k, device_override=None):
        dev_suffix = ""
        if isinstance(k, str):
            k = [k]
        if isinstance(k, dict):
            dev_suffix = ", Device::" + k["device"]
            k = [k["code"]]

        if not dev_suffix and device_override:
            dev_suffix = ", Device::" + device_override

        sec_suffix = ""
        if "MOUSE" in k[0]:
            dev_suffix = ", Device::MOUSE"
        if len(k) == 2:
            if not dev_suffix:
                dev_suffix = ", Device::KEYBOARD"
            sec_suffix = ", " + (sanitize_mapped_key(k[1]) or "NO_OP") 
        return "IndKeyMap(" + (sanitize_mapped_key(k[0]) or "NO_OP") + dev_suffix + sec_suffix + ")"

    for ln in ["base"] + lnames:
        layer = layers.get(ln, {})
        device_override = layer.get("device_override", None)
        code += f"""IndKeyMap {ln}_map[] = {{""" + ", ".join([keymap_to_indkeymap(k, device_override) for k in make_state_map(layout_primary, "right", layer)[-1]]) + "};\n"
        code += f"""IndKeyMap {ln}_map_sec[] = {{""" + ", ".join([keymap_to_indkeymap(k, device_override) for k in make_state_map(layout_secondary, "left", layer)[-1]]) + "};\n"
        code += f"""IndKeyMap curr_map[] = {{""" + ", ".join([keymap_to_indkeymap(k, device_override) for k in make_state_map(layout_primary, "right", layer)[-1]]) + "};\n"
        code += f"""IndKeyMap curr_map_sec[] = {{""" + ", ".join([keymap_to_indkeymap(k, device_override) for k in make_state_map(layout_secondary, "left", layer)[-1]]) + "};\n"
        break

    code += """
void setup() {
    Serial1.begin(115200);
    Serial.begin(115200);
    pinMode(LED_BUILTIN_TX,INPUT);
    pinMode(LED_BUILTIN_RX,INPUT);
    \n"""

    for row_num in row_pin_map:
        code += f"  setup_output({row(row_num)});\n"

    for col_num in col_pin_map:
        code += f"  setup_input({col(col_num)});\n"

    code += "  Keyboard.begin();\n delay(1300);\n}"

    code += """\nvoid loop() {"""

    code += f"""
    int start = millis();
    
    for (int i = 0; i < {num_keys}; i++) {{
      curr_map[i] = base_map[i];
      curr_map_sec[i] = base_map_sec[i];
    }}
"""

    code +="""

    auto at_least_one_downed_after = false;
    auto at_least_one_downed_before = false;

    bool process_seconday = false;
    //Serial.println(millis());
    """

    code += f"""
    if (Serial1.available()) {{
        int tots = Serial1.readBytesUntil('{nl}', state_sec, {num_keys_sec} + 10);
        if (tots == {num_keys_sec}) {{
            //Serial.println(tots);
            //Serial.write(state_sec, tots);
            //Serial.println();
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
        code += f"  at_least_one_downed_after = (at_least_one_downed_after || {tracker_name}[i].update({state_name}[i] == '1'));{NL}" + NL
        code += f"  at_least_one_downed_before = (at_least_one_downed_before || ({tracker_name}[i].state == KeyState::KEY_DOWN));{NL}}}" + NL

    for ln, layer in layers.items():
        half = layer["key"]["half"]
        suffixes = [""] if half == "right" else ["_sec"]
        if half == "both":
            suffixes = ["", "_sec"]
        for suffix in suffixes:
            r, c = layer["key"]["key"]
            hold = layer["key"]["hold"]
            le_idx = row_col_to_state_idx[rckey(r, c)]
            le_name = f"trackers{suffix}[{le_idx}]"
            if not hold:
                code += f"""if ({le_name}.primary_down()) {{"""
            else:
                code += f"""if ({le_name}.long_down() || {le_name}.down_longer_than_others(at_least_one_downed_after)) {{"""

            layer = layers.get(ln, {})
            device_override = layer.get("device_override", None)
            code += "; ".join([f"curr_map[{i}]="+keymap_to_indkeymap(k, device_override) for i, k in enumerate(make_state_map(layout_primary, "right", layer)[-1])]) + ";\n"
            code += "; ".join([f"curr_map_sec[{i}]="+keymap_to_indkeymap(k, device_override) for i, k in enumerate(make_state_map(layout_secondary, "left", layer)[-1])]) + ";};\n"

    for suffix in ["", "_sec"]:
        code += f"for (int i = 0; i < {num_keys}; i++) {{" + NL
        code += f"if(curr_map{suffix}[i].primary.code != curr_map{suffix}[i].secondary) {{" + NL
        code += f"  trackers{suffix}[i].emit(curr_map{suffix}[i], at_least_one_downed_after, at_least_one_downed_before);{NL}}}}}" + NL

    for suffix in ["", "_sec"]:
        code += f"for (int i = 0; i < {num_keys}; i++) {{" + NL
        code += f"if(curr_map{suffix}[i].primary.code == curr_map{suffix}[i].secondary) {{" + NL
        code += f"  trackers{suffix}[i].emit(curr_map{suffix}[i], at_least_one_downed_after, at_least_one_downed_before);{NL}}}}}" + NL
        

    code += "\n }"

    return code