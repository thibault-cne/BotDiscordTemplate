"""
    Author : @Vladou
    Discord : Thibô#0001
"""

import discord
from discord.ext import commands

from cogs._corePrefix import get_guild_prefix
from cogs._coreJson import read_json


class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        #on empeche le bot de se répondre a lui même
        if message.author.id == self.client.user.id:
            return
        
        guild_id = str(message.guild.id)
        prefix = get_guild_prefix(self.client, guild_id)
        data = read_json('disabledCommands')
        
        if f"<@!{self.client.user.id}>" in message.content:
            prefixEmbed = discord.Embed(
                title='Prefixe du serveur :',
                color=self.client.color['WHITE']
            )
            
            description = f"Le prefixe sur ce serveur est : `{prefix}`."
            prefixEmbed.description = description

            await message.channel.send(embed=prefixEmbed)
            return
        
        if guild_id in data and message.content[len(prefix):] in data[guild_id]['disabledCommands']:
            return


def setup(client):
    client.add_cog(Events(client))