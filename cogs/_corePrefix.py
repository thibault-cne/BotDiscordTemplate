"""
    Author : @Vladou
    Discord : Thibô#0001
"""

from cogs._coreJson import read_json
from discord.ext import commands


def get_prefix(client, message):
    """
        Fonction qui permet de récupérer le prefixe lié
        au discord ou le message a été envoyé.

        Parameters:
            - client (client) : le client discord
            - message (message) : le message envoyé
        
        Returns :
            - prefix (commands prefix) : renvoi le prefix
    """

    guild_id = str(message.guild.id)
    data = read_json('prefixes')

    if guild_id in data:
        return commands.when_mentioned_or(data[str(guild_id)])(client, message)
    else:
        return commands.when_mentioned_or(client.defaultPrefix)(client, message)


def get_guild_prefix(client, guild_id):
    """
        Fonction qui permet de récupérer le prefixe lié
        au discord ou le message a été envoyé.

        Parameters:
            - client (client) : le client discord
            - guild_id (guild_id) : id du discord duquel on veut récupérer le prefixe
        
        Returns :
            - prefix (discord prefix) : renvoi le prefixe
    """

    data = read_json('prefixes')
    
    if guild_id in data:
        return str(data[guild_id])
    else:
        return str(client.defaultPrefix)