# make a function that filters dataset based on specified col

def filter_data(data, col, operator, value, chunked_filter=False, chunk_size=1000):
    result = []

    def row_matches(row):
        # preprocess input value
        try: # handle numeric comparisons
            value_num = float(value)
            value_type = 'numeric'
        except ValueError: # fallback to string comparisons, lowercase and strip spaces
            # if user filters by country "Mexico", it should match " mexico ", "MEXICO", etc.
            value_str = str(value).lower().strip()
            value_type = 'string'

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
        elif value_type == 'numeric' and cell_type == 'numeric':
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

        
        # Fallback comparison (string or other types)
        else: 
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
    
        return False 

    if chunked_filter: 
        # Process data in chunks using chunked_csv_reader
        for chunk in chunked_csv_reader(data, chunk_size=chunk_size):
            for row in chunk:
                if row_matches(row):
                    result.append(row)

    else:
        # Original behavior on full data list 
        for row in data:
            if row_matches(row):
                result.append(row)
    

