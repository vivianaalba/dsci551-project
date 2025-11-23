# import our own modules to help with loading and parsing file
from validate_path import validate_file
from parser import parse_csv_line, parse_field
from chunked_csv_read import chunked_csv_reader

######## IMPLEMENTING CHUNK SIZE READING ########
# this would be used if we want to omit the file size check and always perform chunked reading
# chunked reading for loading and parsing works file for small and large files
# serves as scaling feature -- handle larger files that do not fit in memory
def read_csv(file_path, chunk_size=1000, table_format=False):
    # Validate file existence or path correctness 
    if not validate_file(file_path):
        return False

    data = []

    # If chunk_size is None or 0, fallback to full file read
    if not chunk_size:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
        headers = parse_csv_line(lines[0])
        headers = [h.lower() for h in headers]

        for line in lines[1:]:
            if not line.strip():
                continue  # skip empty lines
            values = parse_csv_line(line)

            # Ensure row length matches headers
            if len(values) < len(headers):
                values += [''] * (len(headers) - len(values))
            elif len(values) > len(headers):
                values = values[:len(headers)]

            # Clean values: strip + lowercase for strings
            cleaned_values = []
            for v in values:
                if isinstance(v, str):
                    cleaned = v.strip()
                    # Try numeric normalization
                    try:
                        normalized = cleaned.replace(",", ".")
                        cleaned_values.append(float(normalized))
                        continue
                    except ValueError:
                        cleaned_values.append(cleaned.lower())
                else:
                    cleaned_values.append(v)

            row_dict = {k: v for k, v in zip(headers, cleaned_values)}
            data.append(row_dict)

        if table_format:
            table = [headers] + [[row[h] for h in headers] for row in data]
            return table
        else:
            return data
            
    # For chunked reading, use chunked_csv_reader
    for chunk in chunked_csv_reader(file_path, chunk_size=chunk_size):
        # normalize keys for all rows in chunk
        # helps with comparisons for our other functions such as filter, join, etc.
        new_chunk = []
        for row in chunk:
            clean_row = {}
            for k, v in row.items():
                key = k.lower().strip()
                if isinstance(v, str):
                    cleaned = v.strip()
                    # try numeric normalization
                    try:
                        normalized = cleaned.replace(",", ".")
                        clean_row[key] = float(normalized)
                    except ValueError:
                        clean_row[key] = cleaned.lower()
                else:
                    clean_row[key] = v
            new_chunk.append(clean_row)
        if table_format:
            headers = list(new_chunk[0].keys()) if new_chunk else []
            # normalize headers by lowercasing and stripping
            headers = [h.lower().strip() for h in headers]

            table_rows = []
            for row in new_chunk:
                row_list = []
                for h in headers:
                    row_list.append(row.get(h, ''))
                table_rows.append(row_list)

            table_chunk = [headers] + table_rows
            data.append(table_chunk)  # can accumulate all chunks
        else:
            data.extend(new_chunk)  # flatten chunks into one list

    if table_format:
        # flatten tables from all chunks into one single table
        if not data:
            return []
        headers = data[0][0]
        rows = []
        for table_chunk in data:
            rows.extend(table_chunk[1:])
        table = [headers] + rows
        return table
    else:
        return data
