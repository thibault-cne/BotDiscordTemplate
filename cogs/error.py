"""
    Author : @Vladou
    Discord : Thibô#0001
"""

import discord
import traceback
from discord.ext import commands

from cogs._coreJson import read_json
from cogs._corePrefix import get_guild_prefix

class CommandErrorHandler(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        async with ctx.typing():
            errorEmbed = discord.Embed(
            title = ":pushpin: **Erreur**",
            color = self.client.color["RED"]
            )
            if isinstance(error, commands.CommandNotFound):
                errorEmbed.description = "Cette commande n'existe pas"
            
            elif isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
                command = ctx.command
                guild_id = str(ctx.guild.id)
                errorText = f"Une erreur est survenue lors de l'utilisation de la commande : ```{command.name}```\n"
                errorText += f"Voici l'utilisation classique de la commande **{command.name}**\n\
                ```{get_guild_prefix(self.client, guild_id)}{command.name} {command.usage if not None else ''}```\n\n\
                Pour plus d'information utiliser la commande ```help```"

                errorEmbed.description = errorText

            elif isinstance(error, commands.MissingAnyRole):
                errorEmbed.description = "Vous n'avez pas les permission requise pour effectuer cette commande"
            
            elif isinstance(error, commands.DisabledCommand):
                errorEmbed.description = f"La commande `{ctx.command.name}` est désactivée"
            
            elif isinstance(error, commands.CheckFailure):
                command = ctx.command
                guild_id = str(ctx.guild.id)
                data = read_json('disabledCommands')

                if guild_id in data and command.name in data[guild_id]['disabledCommands']:
                    errorEmbed.description = f"La commande `{ctx.command.name}` a été désactivée.\n\
                    Utilisez la commande `{get_guild_prefix(self.client, guild_id)}activer {ctx.command.name} pour la reactiver."
                else:
                    errorEmbed.description = f"Une erreur est survenue dans la commande `{ctx.command}`: \n"
                    exception = traceback.format_exception(type(error), error, error.__traceback__)
                    str_exception = ""
                    for string in exception:
                        str_exception += string
                    
                    errorEmbed.description+=f"```{str_exception}```"
            
            else:
                errorEmbed.description = f"Une erreur est survenue dans la commande `{ctx.command}`: \n"
                exception = traceback.format_exception(type(error), error, error.__traceback__)
                str_exception = ""
                for string in exception:
                    str_exception += string
                
                errorEmbed.description+=f"```{str_exception}```"

            await ctx.send(embed=errorEmbed)


def setup(client):
    client.add_cog(CommandErrorHandler(client))