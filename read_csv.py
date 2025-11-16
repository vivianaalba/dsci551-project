from validate_path import validate_file
from parser import parse_csv_line

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




