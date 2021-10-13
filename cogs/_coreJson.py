"""
    Author : @Vladou
    Discord : Thibô#0001
"""

import json
from pathlib import Path


def get_path():
    """
        Function which send back the path of the first parents
        from the current forlder.

        Parameters :
            None

        Returns :
            - cwd (string) : path of the first parent
    """

    cwd = Path(__file__).parents[1]
    cwd = str(cwd)
    return cwd


def read_json(filename):
    """
        Function to read a json file

        Parameters :
            - filename (string) : filename
        
        Returns :
            - data (dict) : data stored in the json file
    """

    cwd = get_path()
    with open(cwd+'/bot_config/'+filename+'.json', 'r') as file:
        data = json.load(file)
    return data


def write_json(data, filename):
    """
        Function to modigy a json file.

        Parameters :
            - data (dict) : modification of the json file
            - filename (string) : name of the json file to modify
        
        Returns :
            None
    """

    cwd = get_path()

    with open(cwd+'/bot_config/'+filename+'.json', 'w') as file:
        json.dump(data, file, indent=4)