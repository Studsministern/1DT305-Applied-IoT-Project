def get_env():
    # Using json to get WiFi credential environment variables
    import json
    
    env = {}
    path = '../env.json'

    try:
        f = open(path) # Opening JSON file
        env = json.load(f) # returns JSON object as a dictionary
        f.close() # Closing the JSON file
    except OSError:
        raise OSError('The file env.json could not be found on the path \'{}\'.'.format(path))
    except Exception as err:
        print('Something went wrong with the file on the path \'{}\'.'.format(path))
        raise err

    return env