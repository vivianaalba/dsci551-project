# Basic group by function
def group_by(data, key_func):
    groups = {}
    for item in data:
        key = key_func(item)
        if key not in groups:
            groups[key] = []
        groups[key].append(item)
    return groups

# Group by with aggregation
def group_by_aggregate(data, key_func, agg_func):
    groups = {}
    for item in data:
        key = key_func(item)
        if key not in groups:
            groups[key] = []
        groups[key].append(item)
    # Apply aggregation function to each group
    return {k: agg_func(v) for k, v in groups.items()}

# Nested group by (multi-level grouping)
def nested_group_by(data, key_funcs, agg_func=None):
    if not key_funcs:
        # If aggregation function is provided, apply it
        return agg_func(data) if agg_func else data
    key_func = key_funcs[0]
    groups = {}
    for item in data:
        key = key_func(item)
        if key not in groups:
            groups[key] = []
        groups[key].append(item)
    # Recursively group by the next key
    return {k: nested_group_by(v, key_funcs[1:], agg_func) for k, v in groups.items()}

# Example usage
data = [
    ("Alice", "NY", "HR", 100),
    ("Bob", "LA", "IT", 200),
    ("Charlie", "NY", "IT", 150),
    ("David", "LA", "HR", 120),
    ("Eve", "NY", "HR", 130)
]

# Group by city
print(group_by(data, lambda x: x[1]))

# Group by city, sum amounts
print(group_by_aggregate(data, lambda x: x[1], lambda items: sum(x[3] for x in items)))

# Nested group by: city, then department, sum amounts
print(nested_group_by(
    data,
    key_funcs=[lambda x: x[1], lambda x: x[2]],
    agg_func=lambda items: sum(x[3] for x in items)
))
