def chunked_csv_reader(file_path, chunk_size=1000):
    """
    Generator: Processes a large CSV file and yields lists of row dicts in batches.
    Uses record_generator and parse_csv_line for robust parsing.
    """
    from parser import record_generator, parse_csv_line
    from validate_path import validate_file
    
    if not validate_file(file_path):
        raise FileNotFoundError(f"{file_path} not found.")

    with open(file_path, "r", encoding="utf-8", newline="") as f:
        records = record_generator(f)
        try:
            headers = parse_csv_line(next(records))
        except StopIteration:
            return  # Empty file

        chunk = []
        for record in records:
            if not record.strip():
                continue
            values = parse_csv_line(record)
            while len(values) < len(headers):
                values.append("")
            row = dict(zip(headers, values))
            chunk.append(row)
            if len(chunk) == chunk_size:
                yield chunk
                chunk = []
        if chunk:
            yield chunk  # Yield any leftover rows at the end

# Example usage:
for batch in chunked_csv_reader("largefile.csv", chunk_size=500):
    # Here batch is a list of 500 row dicts (or less for the last chunk)
    process(batch)  # Replace with your aggregation/output logic
