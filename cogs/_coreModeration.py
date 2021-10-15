"""
    Author : @Vladou
    Discord : Thibô#0001
"""


from typing import NewType


def removeUser(jsonDict, user_id, guild_id):
    """
        Function to remove a user from the blackList of the guild

        Parameters :
            - jsonDict (dict) : content of the blackList.json file
            - user_id (user id) : discord id of the un-blacklisted user
            - guild_id (guild id) : discord id of the guild of the blacklisted member

        Returns :
            - dict (dict) : new value of blackList.json file
    """

    new_blackList = []
    for tuples in jsonDict[guild_id]["BlackListMember"]:
        if str(tuples[0]) == str(user_id):
            continue
        else:
            new_blackList.append(tuples)
    
    jsonDict[guild_id]["BlackListMember"] = new_blackList
    return jsonDict


def searchUser(jsonDict, user_id, guild_id):
    """
        Function to search a user in the blackList of the guild

        Parameters :
            - jsonDict (dict) : content of the blackList.json file
            - user_id (user id) : discord id of the un-blacklisted user
            - guild_id (guild id) : discord id of the guild of the blacklisted member

        Returns :
            - state (Bool) : boolean of the needed statement
    """

    state = False

    for tuples in jsonDict[guild_id]["BlackListMember"]:
        state = state or str(tuples[0]) == str(user_id)
    
    return state

