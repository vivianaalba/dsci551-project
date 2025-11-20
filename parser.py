# parse_object does the following:
# Converts numeric fields to int or float
# Recognizes colons as a distinct token
# Parses simple objects formatted as {key: value, ...}

def parse_object(field):
    # Remove surrounding braces if present
    content = field.strip()[1:-1].strip()
    obj = {}
    if not content:
        return obj # empty object 
    # Split by commas for pairs
    pairs = content.split(',')
    for pair in pairs:
        if ':' in pair:
            key, value = pair.split(':', 1)
            key = key.strip().strip('"').strip("'")
            # Delegate value parsing to parse_field for conversion
            value = parse_field(value)
            obj[key] = value 
        else:
            # Malformed pair, set value as None
            obj[pair.strip()] = None 
    return obj 

def parse_field(field):
    field = field.strip()
    if field == '':
        return None
    if field == ':':
        return field 
    # Try parsing as integer
    try:
        return int(field)
    except ValueError:
        pass 
    # Try parsing as float
    try:
        return float(field)
    except ValueError:
        pass 
    # Try custom object parse
    if field.startswith('{') and field.endswith('}'):
        return parse_object(field)
    # Remove quotes and unescape inner quotes for quoted strings
    if field.startswith('"') and field.endswith('"'):
        return field[1:-1].replace('""', '"')
    return field 

def parse_csv_line(line):
    fields = []
    field = ''
    inside_quotes = False
    i = 0
    while i < len(line):
        char = line[i]
        if char == '"':
            # If inside quotes, check for escaped quote
            if inside_quotes and i + 1 < len(line) and line[i + 1] == '"':
                field += '"'
                i += 1  # Skip the escaped quote
            else:
                inside_quotes = not inside_quotes
        elif char == ',' and not inside_quotes:
            fields.append(parse_field(field))
            field = ''
        else:
            field += char
        i += 1
    fields.append(parse_field(field))  # Add the last field
    return fields


