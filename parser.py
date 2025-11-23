# parse_object does the following:
# Converts numeric fields to int or float
# Recognizes colons as a distinct token
# Parses simple objects formatted as {key: value, ...}

def parse_object(field):
    # remove surrounding braces if present
    content = field.strip()[1:-1].strip()
    obj = {}
    if not content:
        return obj  # empty object

    # split by commas for pairs
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
    # Handle None explicitly
    if field is None:
        return None

    # If it's already numeric, keep it
    if isinstance(field, (int, float)):
        return field

    # Convert to string safely
    field = str(field).strip()

    # Empty cell
    if field == '':
        return None

    # Colon by itself
    if field == ':':
        return field

    # ---- NUMERIC NORMALIZATION ----
    # normalizing numbers with diff formats will help when comparing vals
    # also accounts for numbers that are in "European" format

    # Remove spaces: "1 000" → "1000"
    cleaned = field.replace(" ", "")

    # Handle thousands separators & decimal commas
    if "," in cleaned and "." in cleaned:
        # If comma appears AFTER last dot → decimal comma
        if cleaned.rfind(",") > cleaned.rfind("."):
            cleaned = cleaned.replace(".", "")  # remove thousands dots
            cleaned = cleaned.replace(",", ".")  # decimal comma → dot
        else:
            # U.S. thousand comma
            cleaned = cleaned.replace(",", "")
    elif "," in cleaned:
        # Only comma exists → treat as decimal comma
        cleaned = cleaned.replace(",", ".")

    # try to make the val an integer first
    try:
        return int(cleaned)
    except ValueError:
        pass

    # then try float
    try:
        return float(cleaned)
    except ValueError:
        pass

    # try parsing object
    if field.startswith('{') and field.endswith('}'):
        return parse_object(field)

    # Handle quoted strings
    # some fields may look like "Yogurt, buttermilk, or whey"
    # must handle these commas so that they don't split the object incorrectly
    if field.startswith('"') and field.endswith('"'):
        return field[1:-1].replace('""', '"')

    # default: return cleaned string
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
                i += 1  # skip escaped quote
            else:
                inside_quotes = not inside_quotes

        elif char == ',' and not inside_quotes:
            fields.append(parse_field(field))
            field = ''

        else:
            field += char

        i += 1

    fields.append(parse_field(field))  # last field
    return fields

