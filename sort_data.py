# make a function that sorts dataset based on specified col
# asc will be default, can enter asc (smallest to largest) or desc (largest to smallest)
def sort_data(data, col, order_by="asc"):
    if order_by not in ["asc", "desc"]:
        return "Please enter a valid order by clause: 'asc' or 'desc'."
    
    # extract value from data
    def get_value(row):
        try:
            return float(row[col]) # handle numeric comparisons
        except ValueError:
            return row[col] # keep as strings if not numbers

    sorted_data = []

    if chunked_sort:
        # Gather all rows from chunks for global sorting
        for chunk in chunked_csv_reader(data, chunk_size = chunk_size):
            sorted_data.extend(chunk)

        # Now sort the combined data
        sorted_data = quicksort(sorted_Data, key = get_value)
    else:
        sorted_Data = quicksort(data, key = get_value)

    # reverse if descending
    if order_by == "desc":
        sorted_data = sorted_data[::-1]

    return sorted_data


def quicksort(arr, key):
    if len(arr) <= 1: #if array less than 1, do not sort futher
        return arr
    else:
        pivot = arr[len(arr) // 2]
        pivot_val = key(pivot)

        left = [x for x in arr if key(x) < pivot_val] # nums less than pivot
        middle = [x for x in arr if key(x) == pivot_val] # nums equal to pivot
        right = [x for x in arr if key(x) > pivot_val] # nums greater than pivot
        
        return quicksort(left, key) + middle + quicksort(right, key)