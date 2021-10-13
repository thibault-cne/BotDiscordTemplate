"""
    Author : @Vladou
    Discord : Thibô#0001
"""

import discord
from discord.ext import commands
import os

from cogs._coreJson import read_json, write_json
from cogs._corePrefix import get_guild_prefix
from discord.ext.commands.errors import ExtensionNotLoaded




class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        name='reload',
        description='Permet de recharger tout les cogs.'
    )
    @commands.is_owner()
    async def reload(self, ctx):
        loadingText = ""
        
        async with ctx.typing():
            reloadEmbed = discord.Embed(
                title="Reload de tous les cogs",
                color=self.client.color["ORANGE"]
            )
            
            for filename in os.listdir("./cogs"):
                if filename.startswith("_"):
                    continue
                elif filename.endswith(".py"):
                    try:
                        self.client.unload_extension(f"cogs.{filename[:-3]}")
                        self.client.load_extension(f"cogs.{filename[:-3]}")
                        loadingText += f"Cog ```{filename[:-3]}``` a bien été rechargé \n ----- \n"
                    except commands.ExtensionNotLoaded:
                        self.client.load_extension(f"cogs.{filename[:-3]}")
                        loadingText += f"Cog ```{filename[:-3]}``` a bien été chargé \n ----- \n"

            reloadEmbed.description = loadingText
        
        await ctx.send(embed=reloadEmbed)


    @commands.command(
        name='unload',
        description="Permet d'unload un cog",
        usage="<cog>"
    )
    @commands.is_owner()
    async def unload(self, ctx, cog):
        cogText = ""
        cog += ".py"
        
        async with ctx.typing():
            unloadEmbed = discord.Embed(
                title="Unload un cog",
                color=self.client.color["ORANGE"]
            )

            if cog not in os.listdir("./cogs"):
                cogText += f"Le cog `{cog}` n'existe pas"
            else:
                try:
                    self.client.unload_extension(f"cogs.{cog[:-3]}")
                    cogText += f"Le cog `{cog}` a bien été unload"
                except ExtensionNotLoaded:
                    cogText += f"Le cog `{cog}` n'était pas chargé"
            
            unloadEmbed.description = cogText
        await ctx.send(embed=unloadEmbed)
    
    @commands.command(
        name='disconnect',
        description="Permet de deconnecter le bot"
    )
    @commands.is_owner()
    async def disconnect(self, ctx):
        disconnectEmbed = discord.Embed(
            title="Deconnexion",
            description=f"`{self.client.user.name}` : je me déconnecte",
            color=self.client.color["ORANGE"]
        )
        await ctx.send(embed=disconnectEmbed)
        await self.client.logout()


    @commands.command(
        name='prefix',
        description='Permet de changer le prefix utiliser pour les commandes sur ce discord.',
        usage='<prefix>'
    )
    @commands.has_guild_permissions(administrator=True)
    async def prefix(self, ctx, prefix):
        data = read_json('prefixes')
        guild_id = str(ctx.guild.id)

        if prefix == 'defaut':
            del data[guild_id]
            description = f"Le prefixe sur ce discord a bien été changé en : `{self.client.defaultPrefix}`."
        else:
            data[guild_id] = prefix
            description = f"Le prefixe sur ce discord a bien été changé en : `{prefix}`.\n\
            Utilise {prefix}prefix defaut pour revenir au prefix da base qui est : {self.client.defaultPrefix}."

        write_json(data, 'prefixes')

        prefixEmbed = discord.Embed(
            title='Modification du prefixe :',
            description=description,
            color=self.client.color['DARK_GOLD']
        )

        await ctx.send(embed=prefixEmbed)
    
    @commands.command(
        name='purge',
        description='Supprime les derniers messages dans le channel',
        usage='[nombre] || de base 1'
    )
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, numbre=1):
        await ctx.channel.purge(limit=numbre)

    @commands.command(
        name='desactiver',
        description='permet de desactiver une commande sur le discord',
        usage='<commande>'
    )
    @commands.has_permissions(administrator=True)
    async def desactiver(self, ctx, command):
        guild_id = str(ctx.guild.id)
        data = read_json('disabledCommands')
        if command not in [i.name for i in self.client.commands]:
            errorEmbed = discord.Embed(
                title='Erreur',
                description=f"La commande, {command} n'existe pas.\n\
                Vous pouvez consulter la liste des commandes avec `{get_guild_prefix(self.client, guild_id)}help`.",
                color=self.client.color['RED']
            )
            await ctx.send(embed=errorEmbed)
        else:
            commandIndex = [i.name for i in self.client.commands].index(command)
            commandObject = [i for i in self.client.commands][commandIndex]

            disableEmbed=discord.Embed(
                title='Désactivation :',
                color=self.client.color['GREEN']
            )
            if commandObject.cog.qualified_name == "Admin":
                errorEmbed = discord.Embed(
                    title='Erreur',
                    description=f"La commande, {command} ne peut pas être activée/désactivée.",
                    color=self.client.color['RED']
                )
                await ctx.send(embed=errorEmbed)
                return
            if guild_id in data:
                if command in data[guild_id]['disabledCommands']:
                    disableEmbed.description = f"La commande`{command}` est déjà désactivée \
                    sur ce serveur.\n\
                    Vous pouvez voir la liste des commandes désactivé avec la commande \
                    `{get_guild_prefix(self.client, guild_id)}cmd_desactivée`."
                    disableEmbed.color = self.clien.color['RED']
                else:
                    disableEmbed.description = f"La commande `{command}` a bien été désactivé sur ce discord.\n\
                    Vous pouvez consulter la liste des fonction désactivé avec\
                    {get_guild_prefix(self.client, guild_id)}cmd_desactive."

                    data[guild_id]['disabledCommands'].append(command)
                    write_json(data, 'disabledCommands')
            else:
                disableEmbed.description = f"La commande `{command}` a bien été désactivé sur ce discord.\n\
                Vous pouvez consulter la liste des fonction désactivé avec\
                {get_guild_prefix(self.client, guild_id)}cmd_desactive."

                data[guild_id] = {}
                data[guild_id]['disabledCommands'] = [command]
                write_json(data, 'disabledCommands')

            await ctx.send(embed=disableEmbed)
        
    @commands.command(
        name='activer',
        description="permet d'activer une commande sur le discord",
        usage='<commande>'
    )
    @commands.has_permissions(administrator=True)
    async def activer(self, ctx, command):
        guild_id = str(ctx.guild.id)
        data = read_json('disabledCommands')
        if command not in [i.name for i in self.client.commands]:
            errorEmbed = discord.Embed(
                title='Erreur',
                description=f"La commande, {command} n'existe pas.\n\
                Vous pouvez consulter la liste des commandes avec `{get_guild_prefix(self.client, guild_id)}help`.",
                color=self.client.color['RED']
            )
            await ctx.send(embed=errorEmbed)
        else:
            commandIndex = [i.name for i in self.client.commands].index(command)
            commandObject = [i for i in self.client.commands][commandIndex]

            disableEmbed=discord.Embed(
                title='Désactivation :',
                color=self.client.color['GREEN']
            )

            if commandObject.cog.qualified_name == "Admin":
                errorEmbed = discord.Embed(
                    title='Erreur',
                    description=f"La commande, {command} ne peut pas être activée/desactivée",
                    color=self.client.color['RED']
                )
                await ctx.send(embed=errorEmbed)
                return
            if guild_id in data:
                commandIndex = data[guild_id]['disabledCommands'].index(command)
                if command not in data[guild_id]['disabledCommands']:
                    disableEmbed.description = f"La commande`{command}` est déjà activée \
                    sur ce serveur.\n\
                    Vous pouvez voir la liste des commandes désactivé avec la commande \
                    `{get_guild_prefix(self.client, guild_id)}cmd_desactivée`."
                    disableEmbed.color = self.clien.color['RED']
                else:
                    disableEmbed.description = f"La commande `{command}` a bien été activée sur ce discord.\n\
                    Vous pouvez consulter la liste des fonction désactivé avec\
                    {get_guild_prefix(self.client, guild_id)}cmd_desactive."

                    del data[guild_id]['disabledCommands'][commandIndex]
                    write_json(data, 'disabledCommands')
            else:
                disableEmbed.description = f"La commande`{command}` est déjà activée \
                sur ce serveur.\n\
                Vous pouvez voir la liste des commandes désactivé avec la commande \
                `{get_guild_prefix(self.client, guild_id)}cmd_desactivée`."
                disableEmbed.color = self.clien.color['RED']

            await ctx.send(embed=disableEmbed)
    

    @commands.command(
        name='cmd_desactive',
        description="Permet de voir la liste des commandes désactivée sur le serveur."
    )
    async def cmd_desactive(self, ctx):
        async with ctx.typing():
            data = read_json('disabledCommands')
            guild_id = str(ctx.guild.id)
            disabledStr = ""

            if guild_id in data[guild_id]:
                for command in data[guild_id]:
                    commandIndex = [i.name for i in self.client.commands].index(command)
                    commandObject = [i for i in self.client.commands][commandIndex]

                    disabledStr += f"**{commandObject.name}** - *{commandObject.description}*\n"
            else:
                disabledStr = "Il n'y a aucune commande désactivée."            
            
            disabledEmbed = discord.Embed(
                title="Liste des fonctions désactivée :",
                description=disabledStr,
                color=self.client.color['WHITE']
            )
            
            await ctx.send(embed=disabledEmbed)

def setup(client):
    client.add_cog(Admin(client))