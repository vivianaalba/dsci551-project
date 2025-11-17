# make a function that filters dataset based on specified col
# include conditional retrieval such as AND or OR
def filter_data(data, col, operator, value):
    result = []
    for row in data:
        cell_value = row[col]
        
        try: # handle numeric comparisons
            cell_value = float(cell_value)
            value = float(value)
        except ValueError:
            pass  # keep as strings if not numbers

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