from validate_path import validate_file

# file reading logic
# default headers = None, will use first line of data
# default separator = comma
def read_csv(path: str, headers: list = None, separator:str = ",", table_format=False):
    valid_separators = [",", "|", "\t", ";", " "] 
    
    # make sure file / file name are valid and exist
    if not validate_file(path):
        return False

    # check for valid seperator (from list above)
    if separator not in valid_separators: 
        print("Invalid separator used.")
        return False
    
    # file reading code, line splitting code here
    with open(path, "r") as file:
        lines = file.readlines()
        data = [line.strip().split(separator) for line in lines] # split lines into fields
    
    # if headers list given AND matches the length of the data
    # add headers to data
    if headers:
        if len(headers) != len(data[0]):
            print("Header length does not match data columns.")
            return False
    else:
        headers = data[0]
        data = data[1:] # removes header row from data
    
     # create a list of dicts (like pandas read_csv) -- returns a list of dicts
    data_with_headers = [dict(zip(headers, row)) for row in data[1:]]
    
    # streamlit automatically renders lists of dicts as json
    # return as a table ready format if requested
    if table_format:
        rows = [[row[h] for h in headers] for row in data_with_headers]
        return [headers] + rows  # ready for st.table()
    else:
        return data_with_headers



