from chunked_csv_read import chunked_csv_reader

# make a function that filters dataset based on specified col
# numerical data can get filtered with >, <, >=, <=, ==, !=
# string data can get filtered with ==, !=

def filter_data(data, col, operator, value, chunked_filter=False, chunk_size=1000):
    result = []

    def row_matches(row):
        # preprocess input value
        try: # handle numeric comparisons
            value_num = float(value)
            value_type = 'numeric'
        except ValueError: 
            # fallback to string comparisons, lowercase and strip spaces
            # if user filters by country "Mexico", it should match " mexico ", "MEXICO", etc.
            value_str = str(value).lower().strip()
            value_type = 'string'

        cell_value = row[col]

        # try converting the cell
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
                return True
            elif operator == "!=" and cell_value_num != value_num:
                return True
            elif operator == ">" and cell_value_num > value_num:
                return True
            elif operator == "<" and cell_value_num < value_num:
                return True
            elif operator == ">=" and cell_value_num >= value_num:
                return True
            elif operator == "<=" and cell_value_num <= value_num:
                return True

        
        # FALLBACK STRING OR OTHER TYPE COMPARE
        else:
            if operator == "==" and cell_value == value:
                return True
            elif operator == "!=" and cell_value != value:
                return True
            elif operator == ">" and cell_value > value:
                return True
            elif operator == "<" and cell_value < value:
                return True
            elif operator == ">=" and cell_value >= value:
                return True
            elif operator == "<=" and cell_value <= value:
                return True
    
        return False 

    if chunked_filter: 
        # process data in chunks using chunked_csv_reader
        # split your data into chunks and process each chunk individually with 
        # your functions and then aggregate results from each chunk to get the final results
        for chunk in chunked_csv_reader(data, chunk_size=chunk_size):
            filtered_chunk = [row for row in chunk if row_matches(row)]
            result.extend(filtered_chunk)

    else:
        # Original behavior on full data list 
        filtered_data = [row for row in data if row_matches(row)]
        result.extend(filtered_data)

    return result
    

