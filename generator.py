from layout import row_pin_map, col_pin_map, layout
from snippets import preamble, functions

def row(row_num):
    return f"ROW_{row_num}_OUT"

def col(col_num):
    return f"COLUMN_{col_num}_IN"

def down(row, col):
    return f"d_{row}{col}"

code = ""

code += preamble + "\n"

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
"""

for row_num in row_pin_map:
    code += f"  setup_output({row(row_num)});\n"

for col_num in col_pin_map:
    code += f"  setup_input({col(col_num)});\n"

code += "  Keyboard.begin();\n  delay(1000);\n}"

code += """void loop() {
"""

for row_num, cols in layout.items():
    code += f"  digitalWrite({row(row_num)}, LOW);\n"
    for col_num, mapped_key in cols.items():
        if mapped_key in ["\'", "\\"]:
            mapped_key = "\\" + mapped_key
            mapped_key = f"'{mapped_key}'"

        if len(mapped_key) == 1:
            mapped_key = f"'{mapped_key}'"
        code += f"  check_key({col(col_num)}, {down(row_num, col_num)}, {mapped_key});\n"
    code += f"  digitalWrite({row(row_num)}, HIGH);\n\n"

code += "}"

with open("/mnt/c/Users/janso/OneDrive/Desktop/kbfirmware/kbfirmware.ino", "w") as ff:
    ff.write(code)