# make a function that filters dataset based on specified col
# include conditional retrieval such as AND or OR
def filter_data(data, col, operator, value):
    result = []

    # preprocess input value
    try: # handle numeric comparisons
        value_num = float(value)
        value_type = 'numeric'
    except ValueError: # fallback to string comparisons, lowercase and strip spaces
        # if user filters by country "Mexico", it should match " mexico ", "MEXICO", etc.
        value_str = str(value).lower().strip()
        value_type = 'string'

    for row in data:
        cell_value = row[col]

        # Try converting the cell
        try:
            cell_value_num = float(cell_value)
            cell_type = 'numeric'
        except ValueError:
            cell_value_str = str(cell_value).lower().strip()
            cell_type = 'string'

        # TEXT FILTERING
        if value_type == 'string' and cell_type == 'string':
            if operator == "==" and cell_value_str == value_str:
                result.append(row)
            elif operator == "!=" and cell_value_str != value_str:
                result.append(row)

        # NUMERIC FILTERING
        if value_type == 'numeric' and cell_type == 'numeric':
            if operator == "==" and cell_value_num == value_num:
                result.append(row)
            elif operator == "!=" and cell_value_num != value_num:
                result.append(row)
            elif operator == ">" and cell_value_num > value_num:
                result.append(row)
            elif operator == "<" and cell_value_num < value_num:
                result.append(row)
            elif operator == ">=" and cell_value_num >= value_num:
                result.append(row)
            elif operator == "<=" and cell_value_num <= value_num:
                result.append(row)

        if operator == "==" and cell_value == value:
            result.append(row)
        elif operator == "!=" and cell_value != value:
            result.append(row)
        elif operator == ">" and cell_value > value:
            result.append(row)
        elif operator == "<" and cell_value < value:
            result.append(row)
        elif operator == ">=" and cell_value >= value:
            result.append(row)
        elif operator == "<=" and cell_value <= value:
            result.append(row)
    
    return result
    
# Implementing conditional retrieval AND or OR
def filter_rows(rows, conditions, logic='AND'):
    result = []
    for row in rows:
        checks = []
        for col, op, val in conditions:
            cell_val = row.get(col)
            checks.append(eval_condition(cell_val, op, val))
        if (logic == 'AND' and all(checks)) or (logic == 'OR' and any(checks)):
            result.append(row)
    return result