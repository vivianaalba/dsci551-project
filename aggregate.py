from parser import parse_field
# If using chunked mode, import your chunk reader:
# from chunked_csv_read import chunked_csv_reader


# normalize missing group keys, so that they are grouped together
# chose to do this because missing keys would create many separate groups
# instead of ignoring, we group them under "Unknown"
# missing vals can be important in analysis
def clean_key_value(val):
    if val is None: # our parsing function returns None for missing
        return "Unknown"

    s = str(val).strip().lower() 

    if s in ["", "<na>", "na", "n/a", "none", "null"]: # extras in case output for none differs
        return "Unknown"

    return str(val).strip() # always return cleaned string


# group by function (without aggregation)
def group_by(data, key, chunked_aggregate=False, chunk_size=1000):
    groups = {}

    for row in data:
        raw_val = row.get(key)
        key_val = clean_key_value(raw_val)   # clean value

        if key_val not in groups:
            groups[key_val] = []
        groups[key_val].append(row)

    return groups


# group by (with aggregation)
def group_by_aggregate(data, group_col, agg_col, agg_func, chunked_aggregate=False, chunk_size=1000):
    groups = group_by(data, group_col, chunked_aggregate=chunked_aggregate, chunk_size=chunk_size)
    result = {}

    for key_val, rows in groups.items():
        key_val = clean_key_value(key_val)   # CLEAN AGAIN FOR SAFETY

        try:
            numeric_vals = [float(parse_field(r[agg_col])) for r in rows]
        except:
            numeric_vals = [parse_field(r[agg_col]) for r in rows]

        result[key_val] = agg_func(numeric_vals)

    return result


# ---- Nested group by (multi-level grouping) ----
def nested_group_by(data, key_funcs, agg_func=None, chunked_aggregate=False, chunk_size=1000):
    if not key_funcs:
        return agg_func(data) if agg_func else data

    key_func = key_funcs[0]
    groups = {}

    if chunked_aggregate:
        for chunk in chunked_csv_reader(data, chunk_size=chunk_size):
            for item in chunk:
                raw_key = key_func(item)
                key = clean_key_value(raw_key)   # CLEAN GROUP KEY
                if key not in groups:
                    groups[key] = []
                groups[key].append(item)
    else:
        for item in data:
            raw_key = key_func(item)
            key = clean_key_value(raw_key)       # CLEAN GROUP KEY
            if key not in groups:
                groups[key] = []
            groups[key].append(item)

    return {k: nested_group_by(v, key_funcs[1:], agg_func) for k, v in groups.items()}