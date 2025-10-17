# make a function that filters dataset based on specified col
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