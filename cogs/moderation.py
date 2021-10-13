"""
    Author : @Vladou
    Discord : Thibô#0001
"""

import discord
from discord import guild
from discord import embeds
from discord.ext import commands
import os

from cogs._coreJson import read_json, write_json
from cogs._corePrefix import get_guild_prefix
from discord.ext.commands.errors import ExtensionNotLoaded




class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        name="blacklist",
        description="Permet de blacklist un compte discord du serveur en l'empêchant de se reconnecter sans avoir a le ban.",
        usage="<@member>"
    )
    async def blacklist(self, ctx, user: discord.User):
        blackList = read_json('blackList')

        guild_id = str(ctx.guild.id)
        user_id = str(user.id)

        blackListEmbed = discord.Embed(
            title='Blacklist',
            color=self.client.color['BLACK']
        )
        
        if guild_id not in blackList:
            blackList[guild_id] = {}
            blackList[guild_id]['BlackListMember'] = [user_id]
            await user.kick(reason="Vous êtes blacklist")
            blackListEmbed.description = f"L'utilisateur {user.display_name} à bien été blacklist.\n\
                Vous pouvez consulter la liste des personnes blacklist avec : ```{get_guild_prefix(self.client, guild_id)} blackedmember```\n\
                Vous pouvez un-blacklist un utilisateur en utilisant : ```{get_guild_prefix(self.client, guild_id)} unblacklist```"
            write_json(blackList, 'blackList')
        elif user_id in blackList[guild_id]['BlackListMember']:
            blackListEmbed.description = f"L'utilisateur {user.display_name} à déjà été blacklist.\n\
                Vous pouvez consulter la liste des personnes blacklist avec : ```{get_guild_prefix(self.client, guild_id)} blackedmember```"
        else:
            await user.kick(reason="Vous êtes blacklist")
            blackListEmbed.description = f"L'utilisateur {user.display_name} à bien été blacklist.\n\
                Vous pouvez consulter la liste des personnes blacklist avec : ```{get_guild_prefix(self.client, guild_id)} blackedmember```\n\
                Vous pouvez un-blacklist un utilisateur en utilisant : ```{get_guild_prefix(self.client, guild_id)} unblacklist```"
            blackList[guild_id]['BlackListMember'].append(user_id)
            write_json(blackList, 'blackList')

        await ctx.send(embed=blackListEmbed)
    

    @commands.command(
        name="unblacklist",
        description="Permet de un-blacklist un compte discord du serveur.",
        usage="<@member>"
    )
    async def unblacklist(self, ctx, user: discord.User.id):
        blackList = read_json('blackList')

        guild_id = str(ctx.guild.id)
        user_id = str(user)

        blackListEmbed = discord.Embed(
            title='Un-blacklist',
            color=self.client.color['WHITE']
        )

        if guild_id not in blackList or user_id not in blackList[guild_id]['BlackListMember']:
            blackListEmbed.description = f"L'utilisateur <@{user}> n'est blackliste.\n\
                Vous pouvez consulter la liste des personnes blacklist avec : ```{get_guild_prefix(self.client, guild_id)} blackedmember```\n\
                Vous pouvez le blacklist avec ```{get_guild_prefix(self.client, guild_id)} blacklist```."
        else:
            blackListEmbed.description = f"L'utilisateur <@{user}> à bien été un-blacklist.\n\
                Vous pouvez consulté la liste des personnes blacklist avec ```{get_guild_prefix(self.client, guild_id)} blackedmember```."
            blackList[guild_id]['BlackListMember'].remove(user_id)
            write_json(blackList, 'blackList')

        await ctx.send(embed=blackListEmbed)


    @commands.command(
        name="blackedmember",
        description="Affiche la liste des membres blacklist du discord."
    )
    async def blackedmember(self, ctx):
        guild_id = str(ctx.guild.id)

        blackList = read_json('blackList')
        blackListEmbed = discord.Embed(
            title="Liste des membres blacklist :",
            color=self.client.color['BLACK']
        )
            
        if guild_id not in blackList:
            blackListEmbed.description = "Il n'y a pas de personnes blacklist sur ce serveur"
        else:
            blackListStr = ""
            for user_id in blackList[guild_id]["BlackListMember"]:
                blackListStr += f"<@{user_id}>\n"
            blackListEmbed.description = blackListStr

        await ctx.send(embed=blackListEmbed)


def setup(client):
    client.add_cog(Moderation(client))