from parser import parse_field

# Basic group by function
def group_by(data, key, chunked_aggregate = False, chunk_size = 1000):
    groups = {}

    if chunked_aggregate:
        # Process by chunks
        for chunk in chunked_csv_reader(data, chunk_size = chunk_size):
            for row in chunk:
                ke_val = row.get(key)
                if key_val not in groups:
                    groups[key_val] = []
                groups[key_val].append(row)
    else: 
        for row in data:
            key_val = row.get(key)
            if key_val not in groups:
                groups[key_val] = []
            groups[key_val].append(row)
    return groups

# Group by with aggregation
def group_by_aggregate(data, group_col, agg_col, agg_func, chunked_aggregate = False, chunk_size = 1000):
    groups = group_by(data, group_col, chunked_aggregate = chunked_aggregate, chunk_size = chunk_size)
    result = {}
    for key_val, rows in groups.items():
        try:
            # Try converting aggregation column values to numeric
            numeric_vals = [float(parse_field(r[agg_col])) for r in rows]
        except ValueError:
            numeric_vals = [parse_field(r[agg_col]) for r in rows]

        result[key_val] = agg_func(numeric_vals)
    return result

# Nested group by (multi-level grouping)
def nested_group_by(data, key_funcs, agg_func=None, chunked_aggregate = False, chunk_size = 1000):
    if not key_funcs:
        return agg_func(data) if agg_func else data

    key_func = key_funcs[0]
    groups = {}

    if chunked_aggregate:
        for chunk in chunked_csv_reader(data, chunk_size = chunk_size):
            for item in chunk:
                key = key_func(item)
                if key not in groups:
                    groups[key] = []
                groups[key].append(item)
    else: 
        for item in data:
            key = key_func(item)
            if key not in groups:
                groups[key] = []
            groups[key].append(item)

    return {k: nested_group_by(v, key_funcs[1:], agg_func) for k, v in groups.items()}
