def row(row_num):
    return f"ROW_{row_num}_OUT"

def col(col_num):
    return f"COLUMN_{col_num}_IN"

def down(row, col):
    return f"d_{row}{col}"

def rckey(row, col):
    return f"{row},{col}"

def make_state_map(layout):
    num_keys = 0
    state_idx_to_row_col = {}
    for row_num, cols in layout.items():
        for col_num in cols:
            state_idx_to_row_col[num_keys] = [row_num, col_num]
            num_keys += 1

    row_col_to_state_idx = {rckey(*v): k for k, v in state_idx_to_row_col.items()}
    return num_keys, row_col_to_state_idx


NL = "\n"

def list_to_lines(inlist, indentation):
    if isinstance(inlist, list):
        return "\n".join([" "*indentation + i for i in inlist])
    else:
        return " "*indentation + inlist

def block(preamble, body, indentation=0):
    return f"{' '*indentation}{preamble} {{ \n{list_to_lines(body, indentation + 2)}\n{' '*indentation}}}\n"