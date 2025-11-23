# import our own modules to help with loading and parsing file
from validate_path import validate_file
from parser import parse_csv_line, parse_field
from chunked_csv_read import chunked_csv_reader

######## IMPLEMENTING CHUNK SIZE READING ########
# this would be used if we want to omit the file size check and always perform chunked reading
# chunked reading works file for small and large files
# allows for scaling to handle larger files that do not fit in memory
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
        # Lowercase keys for all rows in chunk
        new_chunk = []
        for row in chunk:
            clean_row = {}
            for k, v in row.items():
                key = k.lower().strip()
                if isinstance(v, str):
                    cleaned = v.strip()
                    # Try numeric normalization
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
            # Lowercase the headers here
            headers = [h.lower().strip() for h in headers]

            table_rows = []
            for row in new_chunk:
                row_list = []
                for h in headers:
                    row_list.append(row.get(h, ''))
                table_rows.append(row_list)

            table_chunk = [headers] + table_rows
            # You can choose to collect all chunks or yield each
            data.append(table_chunk)  # if accumulating all chunks
        else:
            data.extend(new_chunk)  # flatten chunks into one list

    if table_format:
        # Flatten tables from all chunks into a single table
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

# def parse_csv_line(line):

#     # Handles commas inside quotes, ex:
#     # "Cocoa paste, butter, and powder",WORLD,"1,000 mt"
#     # ["Cocoa paste, butter, and powder", "WORLD", "1,000 mt"]

#     fields = []
#     field = ""
#     in_quotes = False

#     i = 0
#     while i < len(line):
#         char = line[i]

#         if char == '"':  # toggle quoted state
#             # Look ahead for double quotes inside a quoted field (escaped quotes)
#             if in_quotes and i + 1 < len(line) and line[i + 1] == '"':
#                 field += '"'  # add one literal quote
#                 i += 1  # skip the next quote
#             else:
#                 in_quotes = not in_quotes  # toggle quote mode

#         elif char == ',' and not in_quotes:
#             # Comma outside quotes = new field
#             fields.append(parse_field(field))
#             field = ""

#         else:
#             field += char
#         i += 1

#     fields.append(parse_field(field))  # last field
#     return fields
