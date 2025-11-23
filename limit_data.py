# returns the first n rows of the dataset
# equivalent to SQL -- SELECT * FROM table LIMIT n;
# implemented on the processed data after reading and parsing

def limit_data(data, n):
    if n is None:
        return data
    if n <= 0:
        return []
    return data[:n]