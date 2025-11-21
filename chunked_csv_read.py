from parser import parse_csv_line
from validate_path import validate_file

def chunked_csv_reader(file_path, chunk_size=1000):
    """
    Generator: Processes a large CSV file and yields lists of row dicts in batches.
    Uses record_generator and parse_csv_line for robust parsing.
    """
    if not validate_file(file_path):
        raise FileNotFoundError(f"File not found or invalid: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        headers_line = f.readline()
        headers = parse_csv_line(headers_line)
        headers = [h.lower().strip() for h in headers] # normalize headers

        chunk = []
        for line in f:
            line = line.strip()
            if not line:
                continue
            values = parse_csv_line(line)
            while len(values) < len(headers):
                values.append('')
            row = dict(zip(headers, values))
            chunk.append(row)
            if len(chunk) == chunk_size:
                yield chunk
                chunk = []
        if chunk:
            yield chunk  # Yield any leftover rows at the end

