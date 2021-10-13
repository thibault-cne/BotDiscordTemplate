"""
    Author : @Vladou
    Discord : Thibô#0001
"""
from discord.ext import commands

from cogs._coreJson import read_json


def check_disabledCommands():
    """
        Function to check if a command is disabled

        Parameters :
            None
        
        Returns :
            - (bool) : whether or not the command is active
    """


    async def predicate(ctx):
        guild_id = str(ctx.guild.id)
        data = read_json('disabledCommands')

        if guild_id not in data:
            return True
        else:
            if ctx.command.name in data[guild_id]['disabledCommands']:
                return False
            else:
                return True
    
    return commands.check(predicate)