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
            fields.append(field)
            field = ''
        else:
            field += char
        i += 1
    fields.append(field)  # Add the last field
    return fields

# Example usage:
csv_line = '123,"hello, world","escaped ""quotes"" inside",456'
parsed_fields = parse_csv_line(csv_line)
print(parsed_fields)
