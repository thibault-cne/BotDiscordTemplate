"""
    Author : @Vladou
    Discord : Thibô#0001
"""

import discord
from discord.ext import commands

import math
import re
from cogs._corePrefix import get_guild_prefix

unecessaryCogs = ['CommandErrorHandler', 'Events']

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client
    

    @commands.command(
        name='help',
        description='Donne la liste de toutes les commandes et une description de chacune.',
        aliases=['h'],
        usage="[Numéro de page/nom de commande]"
    )
    async def help(self, ctx, cog="1"):
        helpEmbed = discord.Embed(
            title="Help commande !",
            color=self.client.color["WHITE"]
        )
        helpEmbed.set_thumbnail(url=ctx.author.avatar_url)

        guild_id = str(ctx.guild.id)
        prefix = get_guild_prefix(self.client, guild_id)
        
        #Get the list of cogs with commands
        cogs = [c for c in self.client.cogs.keys()]
        for _cog in unecessaryCogs:
            cogs.remove(_cog)

        totalPages = math.ceil(len(cogs)/4)

        if re.search(r"\d", str(cog)) is not None:
            cog = int(cog)
            if cog > totalPages or cog < 1:
                errorEmbed = discord.Embed(
                    title="Erreur",
                    description=f"Vous avez rentrez une page invalide, merci de choisir une page entre 1 et {totalPages}",
                    color=self.client.color["RED"]
                )
                await ctx.send(embed=errorEmbed)
                return
            
            helpEmbed.set_footer(text=f"<> - Requis & [] - Optionnel | Cog {cog} sur {totalPages}")
            neededCog = []
            for i in range(4):
                x = i + (cog - 1) * 4
                try:
                    neededCog.append(cogs[x])
                except IndexError:
                    continue
            
            commandList = ""
            for cogs in neededCog:
                commandList += f"```{cogs}```\n"
                for command in self.client.get_cog(cogs).walk_commands():
                    if command.hidden:
                        continue
                    elif command.parent != None:
                        continue

                    commandList += f"**{command.name}** - *{command.description}*\n"
                commandList += "\n\n"
            
            helpEmbed.description = commandList     
        
        elif re.search(r"[a-zA-Z]", str(cog)) is not None:
            lowerCogs = [c.lower() for c in cogs]
            print(cogs)
            print(lowerCogs)
            if cog.lower() not in lowerCogs:
                errorEmbed = discord.Embed(
                    title="Erreur",
                    description=f"Vous avez rentrez un cog invalide.\n\
Pour afficher tous les cogs tapez ```{prefix}help```",
                    color=self.client.color["RED"]
                )
                await ctx.send(embed=errorEmbed)
                return

            helpEmbed.set_footer(text=f"<> - Requis & [] - Optionnel || Cog {lowerCogs.index(cog.lower()) + 1} sur {len(lowerCogs)}")

            helpText = ""
            
            
            for command in self.client.get_cog(cogs[lowerCogs.index(cog.lower())]).walk_commands():
                if command.hidden:
                    continue
                elif command.parents is None:
                    continue
                
                helpText += f"```{command.name}```\n**{command.description}**\n\n"

                if len(command.aliases) > 0:
                    helpText += f"**Aliases :** `{', '.join(command.aliases)}`\n"
                helpText += "\n"

                helpText += f"**Format :** `{prefix}{command.name} \
{command.usage if command.usage is not None else ''}`\n\n"

            helpEmbed.description = helpText

        await ctx.send(embed=helpEmbed)

def setup(client):
    client.add_cog(Help(client))