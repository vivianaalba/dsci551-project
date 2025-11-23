# selects a subset of columns from the dataset
# can project one or multiple cols -- based on col name

def project(data, columns):
    projected = []

    # validate column names
    # however, in dashboad, col names will be displayed to user for selection
    # prevents user errors such as typos or non-existent cols
    if not data:
        return projected

    for col in columns:
        if col not in data[0]:
            raise ValueError(f"Column '{col}' does not exist in dataset.")

    for row in data:
        projected.append({col: row[col] for col in columns})

    return projected
