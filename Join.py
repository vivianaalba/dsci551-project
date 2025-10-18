def join_strings(separator, iterable):
    """
    Join elements of an iterable into a single string using a custom separator.
    This function does not use any libraries or .join() method.
    
    :param separator: The string used to separate each element.
    :param iterable: Any iterable containing string elements.
    :return: A single concatenated string.
    """
    # Validate input types
    if not isinstance(separator, str):
        raise TypeError("Separator must be a string")
    if not hasattr(iterable, '__iter__'):
        raise TypeError("Second argument must be iterable")

    result = ""
    first_element = True

    # Iterate through elements to concatenate manually
    for item in iterable:
        if not isinstance(item, str):
            raise TypeError("All elements in iterable must be strings")

        if not first_element:
            result += separator  # Add separator before each element after the first
        else:
            first_element = False

        result += item  # Concatenate the string

    return result
