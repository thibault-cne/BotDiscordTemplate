"""
    Author : @Vladou
    Discord : Thibô#0001
"""

from cogs._coreJson import read_json
from discord.ext import commands


def get_prefix(client, message):
    """
        Function which returns the prefix of the guild in which the message
        was sent

        Parameters:
            - client (client) : current discord client
            - message (message) : the message sent
        
        Returns :
            - prefix (commands prefix) : the guild prefix
    """

    guild_id = str(message.guild.id)
    data = read_json('prefixes')

    if guild_id in data:
        return commands.when_mentioned_or(data[str(guild_id)])(client, message)
    else:
        return commands.when_mentioned_or(client.defaultPrefix)(client, message)


def get_guild_prefix(client, guild_id):
    """
        Function which returns the prefix of a guild.

        Parameters:
            - client (client) : discord client
            - guild_id (guild_id) : id of the guild you wants to get
                the prefix back
        
        Returns :
            - prefix (discord prefix) : the guild prefix
    """

    data = read_json('prefixes')
    
    if guild_id in data:
        return str(data[guild_id])
    else:
        return str(client.defaultPrefix)