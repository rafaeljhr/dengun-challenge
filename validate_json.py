import json

def validate_json(file_path, required_keys=None):
    try:
        with open(file_path, 'r') as file:
            json_data = json.load(file)
            
            if len(json_data.items()) != 1: # only 1 hour is expected in the json file, for example '05:00 PM'
                print("Error: The number of elements present in the JSON file is different than 1. Only 1 element is expected")
                return False
                
            # quick way of looping https://www.programiz.com/python-programming/methods/built-in/iter
            first_key, first_value = next(iter(json_data.items()))

            if isinstance(first_value, dict): # check if the first element is a dict
                # check if the expected keys are present in the dict, so: DESC,TEMP,FEEL,PRECIP,HUMIDITY,WIND
                # if any key is missing, an error will be raised
                first_value_keys = []
                for key, value in first_value.items(): 
                    first_value_keys.append(key)
                
                are_all_present = True

                for item in required_keys:
                    if item not in first_value_keys:
                        print("Error: The key '" + str(item) + "' is missing in the first key value dictionary!")
                        return False
                
                if are_all_present == False:
                    print("Error: ")
                    
            else:
                print("Error: The first key value should be a dictionary!")
                return False
    
            
            return True
        
    except json.JSONDecodeError as e:
        print("Error decoding JSON: " + str(e))
        return False
    
    except FileNotFoundError:
        print("Error: File '" + file_path + "' not found.")
        return False
    
    except Exception as e:
        print("An unexpected error occurred: " + str(e))
        return False


# run the validation
file_path = './forcast_data.json'
required_keys = ['DESC', 'TEMP', 'FEEL', 'PRECIP', 'HUMIDITY', 'WIND']

print(validate_json(file_path, required_keys))