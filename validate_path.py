import re

# validate file path name and make sure that it is a csv

def validate_name(name):
    # clean name (remove leading spaces)
    name = name.strip()
    forbidden_chars = ["/", "\\", ":", "*", "?", "\"", ">", "<", "|"]

    # check that it is a csv file
    if name[-4:] == ".csv":
        # check that it is a valid file name
        for char in name[:-4]:
            # file cannot contain forbidden chars
             if char in forbidden_chars:
                 print(f"{name} is not a valid csv file name. Please only use valid characters.")
                 return False

        # ile cannot end in period or space
        if name[-5] == "." or name[-5] == " ":
            print(f"{name} is not a valid csv file name. Name cannot end with a space or period.")
            return False
    
        # if all parameters met, it is a valid file name
        return True

    else:
        print(f"{name} is not a valid csv file. Only use .csv file.")
        return False
    

# check that the file exists in our directory
def validate_file(path):
    # extract file name from path
    match = re.search(r'[^\\/]+$', path)
    if match:
        name = match.group(0)
    
    # using extracted file name
    # validate file name, print error for easier debugging
    if not validate_name(name):
        return False
        

    # verify file path by checking that it opens
    try:
        with open(path, 'r') as f:
            return True # return True if file exists
    except FileNotFoundError:
        return False # return False if file does not open (does not exist)
