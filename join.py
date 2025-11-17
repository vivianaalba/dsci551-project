## What are Join Function does 
# Checks that separator is a string
# Verifies all elements of the iterable are strings
# Concatenates the strings with the separator. Appending it before the first element

## Improvements Added 
# Convert non-string elements to string
# Support for generator input
# Improve error message for non-iterable input

# Helper function that takes both file paths and handles joining
def read_and_join(file1, file2, key1, key2, join_type='inner'):
    table1 = read_csv(file1)
    table2 = read_csv(file2)
    if join_type == 'inner':
        return inner_join(table1, table2, key1, key2)
    elif join_type == 'left':
        return left_join(table1, table2, key1, key2)

# Not sure if we need this yet or not
# String join function (can be imported from parser.py)
# def join_strings(separator, iterable):
#     if not isinstance(separator, str):
#         raise TypeError(f"Separator must be a string, got {type(separator)}")
#     if not hasattr(iterable, '__iter__'):
#         raise TypeError(f"Second argument must be iterable, got {type(iterable)}")

#     result = ""
#     first_element = True
#     for item in iterable:
#         item_str = str(item)
#         if not first_element:
#             result += separator
#         else:
#             first_element = False
#         result += item_str
#     return result

# --- SQL-like table join functions ---
# Inner join: Combines only rows with a match in both tables
def inner_join(table1, table2, key1, key2):
    """
    Perform an inner join on two tables (lists of dicts) using specified key(s).
    - key1/key2 can be strings or lists of column names (for composite keys).
    """
    # Validate input types
    if not isinstance(table1, list) or not isinstance(table2, list):
        raise TypeError("Both tables must be lists of dicts.")
    if not (isinstance(key1, str) or isinstance(key1, list)):
        raise TypeError("key1 must be a string or list of strings.")
    if not (isinstance(key2, str) or isinstance(key2, list)):
        raise TypeError("key2 must be a string or list of strings.")

    # Normalize keys for composite key support
    if isinstance(key1, str):
        key1 = [key1]
    if isinstance(key2, str):
        key2 = [key2]

    # Build index for table2 on key2
    index = {}
    for row in table2:
        try:
            index_key = tuple(row[k] for k in key2)
        except KeyError:
            continue  # skip rows missing key
        index.setdefault(index_key, []).append(row)

    result = []
    for row1 in table1:
        try:
            row1_key = tuple(row1[k] for k in key1)
        except KeyError:
            continue  # skip rows missing key
        matched = index.get(row1_key, [])
        for row2 in matched:
            merged_row = merge_rows(row1, row2)
            result.append(merged_row)
    return result

# Left Join: All rows from the left table plus matching info from the right
def left_join(table1, table2, key1, key2):
    """
    Perform a left join on two tables (lists of dicts) using specified key(s).
    """
    if isinstance(key1, str):
        key1 = [key1]
    if isinstance(key2, str):
        key2 = [key2]

    index = {}
    for row in table2:
        try:
            index_key = tuple(row[k] for k in key2)
        except KeyError:
            continue
        index.setdefault(index_key, []).append(row)

    result = []
    for row1 in table1:
        try:
            row1_key = tuple(row1[k] for k in key1)
        except KeyError:
            row1_key = None
        matched = index.get(row1_key, [])
        if matched:
            for row2 in matched:
                merged_row = merge_rows(row1, row2)
                result.append(merged_row)
        else:
            # Merge with placeholders for missing right table
            merged_row = merge_rows(row1, {})
            result.append(merged_row)
    return result


def merge_rows(row1, row2):
    """
    Helper to merge two dicts, avoiding key collisions by suffixing duplicates (left, right).
    """
    merged = {}
    for k in row1:
        merged[k] = row1[k]
    for k in row2:
        if k in merged:
            merged[k + "_right"] = row2[k]
        else:
            merged[k] = row2[k]
    return merged

# --- Optional: Formatted Output using join_strings ---
def join_rows_as_string(row, separator=', '):
    """
    Concatenate all values of a row dict into a string using separator.
    """
    return join_strings(separator, [row[key] for key in row])

# --- Example Usage ---
if __name__ == "__main__":
    # Example tables
    table1 = [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"},
        {"id": 3, "name": "Charlie"}
    ]
    table2 = [
        {"user_id": 1, "score": 88},
        {"user_id": 2, "score": 75},
        {"user_id": 1, "score": 90}
    ]
    inner = inner_join(table1, table2, "id", "user_id")
    left  = left_join(table1, table2, "id", "user_id")
    print("Inner Join Results:")
    for row in inner:
        print(row)
    print("Left Join Results:")
    for row in left:
        print(row)
    print("As String:")
    for row in left:
        print(join_rows_as_string(row))
