def limit_data(data, n):
    """
    Returns the first n rows of the dataset.
    Equivalent to SQL: SELECT * FROM table LIMIT n;
    """
    if n is None:
        return data
    if n <= 0:
        return []
    return data[:n]