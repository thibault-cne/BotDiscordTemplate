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


def setup(client):
    client.add_cog(Admin(client))