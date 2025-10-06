from validate_path import validate_file

# file reading logic
# default headers = None, will use first line of data
# default separator = comma
def read_csv(path: str, headers: list = None, separator:str = ","):
    valid_separators = [",", "|", "\t", ";", " "] 
# make sure file / file name are valid and exist
    if validate_file(path):
        # continue with file reading code here
        if separator in valid_separators: 
            with open(path, "r") as file:
                lines = file.readlines()
                data = [line.strip().split(separator) for line in lines] # split lines into fields
            
            # if headers list given AND matches the length of the data
            # add headers to data
            if headers:
                if len(headers) == len(data[0]):
                    # create a list of dicts (like pandas read_csv)
                    data_with_headers = [dict(zip(headers, row)) for row in data[1:]]
                    return data_with_headers
                else:
                    print("Header length does not match data columns.")
                    return False

            # if no headers provided, assume first row contains headers
            else:
                headers = data[0]
                data_with_headers = [dict(zip(headers, row)) for row in data[1:]]
                return data_with_headers
            
            return data_with_headers
        else:
            print("Invalid separator used.")
            return False # if invalid separator used, return False
        
    else:
        return False # if file path or name are not valid, return False

# currently data prints similar to a json object on streamlit


