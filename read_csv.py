from validate_path import validate_file

# file reading logic
# default headers = None, will use first line of data
# default separator = comma
def read_csv(file_path, table_format=False):
    # make sure file / file name are valid and exist
    if not validate_file(file_path):
        return False

    data = []

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    # First line = header row
    headers = parse_csv_line(lines[0])

    # Parse each data line manually
    for line in lines[1:]:
        if not line.strip():
            continue  # skip empty lines
        values = parse_csv_line(line)
        # pad shorter rows if needed
        while len(values) < len(headers):
            values.append('')
        row_dict = dict(zip(headers, values))
        data.append(row_dict)

    if table_format:
        table = [headers] + [[row[h] for h in headers] for row in data]
        return table
    else:
        return data


def parse_csv_line(line):

    # Handles commas inside quotes, ex:
    # "Cocoa paste, butter, and powder",WORLD,"1,000 mt"
    # ["Cocoa paste, butter, and powder", "WORLD", "1,000 mt"]

    fields = []
    field = ""
    in_quotes = False

    i = 0
    while i < len(line):
        char = line[i]

        if char == '"':  # toggle quoted state
            # Look ahead for double quotes inside a quoted field (escaped quotes)
            if in_quotes and i + 1 < len(line) and line[i + 1] == '"':
                field += '"'  # add one literal quote
                i += 1  # skip the next quote
            else:
                in_quotes = not in_quotes  # toggle quote mode

        elif char == ',' and not in_quotes:
            # Comma outside quotes = new field
            fields.append(field.strip())
            field = ""

        else:
            field += char
        i += 1

    fields.append(field.strip())  # last field
    # remove outer quotes if present
    fields = [f[1:-1] if len(f) >= 2 and f.startswith('"') and f.endswith('"') else f for f in fields]
    return fields



# def read_csv(path: str, headers: list = [], separator:str = ",", table_format=False):
#     valid_separators = [",", "|", "\t", ";", " "] 
    
#     # make sure file / file name are valid and exist
#     if not validate_file(path):
#         return False

#     # check for valid seperator (from list above)
#     if separator not in valid_separators: 
#         print("Invalid separator used.")
#         return False
    
#     # file reading code, line splitting code here
#     with open(path, "r") as file:
#         lines = file.readlines()
#         data = [line.strip().split(separator) for line in lines] # split lines into fields
    
#     # if headers list given AND matches the length of the data
#     # add headers to data
#     if headers:
#         if len(headers) != len(data[0]):
#             print("Header length does not match data columns.")
#             return False
#     else:
#         headers = data[0]
#         data = data[1:] # removes header row from data
    
#      # create a list of dicts (like pandas read_csv) -- returns a list of dicts
#     data_with_headers = [dict(zip(headers, row)) for row in data[1:]]
    
#     # streamlit automatically renders lists of dicts as json
#     # return as a table ready format if requested
#     if table_format:
#         rows = [[row[h] for h in headers] for row in data_with_headers]
#         return [headers] + rows  # ready for st.table()
#     else:
#         return data_with_headers



