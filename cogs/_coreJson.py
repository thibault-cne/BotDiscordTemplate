"""
    Author : @Vladou
    Discord : Thibô#0001
"""

import json
from pathlib import Path


def get_path():
    """
        Fonction qui permet de retrouver le chemin
        d'accès du fichier bot_discord.py

        Returns :
            - cwd (string) : chemin d'accès de bot_discord.py
    """

    cwd = Path(__file__).parents[1]
    cwd = str(cwd)
    return cwd


def read_json(filename):
    """
        Fonction qui permet de lire un fichier .json qui se trouve dans le 
        dossier bot_config.

        Parameters :
            - filename (string) : nom du fichier json a charger
        
        Returns :
            - data (dict) : contenue du fichier json voulue
    """

    cwd = get_path()
    with open(cwd+'/bot_config/'+filename+'.json', 'r') as file:
        data = json.load(file)
    return data


def write_json(data, filename):
    """
        Fonction qui permet de modifier un fichier .json qui se trouve dans le 
        dossier bot_config.

        Parameters :
            - data (dict) : contenue de la modification du json
            - filename (string) : nom du fichier json a charger
    """

    cwd = get_path()

    with open(cwd+'/bot_config/'+filename+'.json', 'w') as file:
        json.dump(data, file, indent=4)