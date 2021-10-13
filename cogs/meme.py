"""
    Author : @Vladou
    Discord : Thibô#0001
"""

import discord
from discord import embeds
from discord.ext import commands

from cogs._coreMeme import get_images, get_meme

class Meme(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(
        name='image',
        description='Permet de renvoyer une image suivant le theme demandé.',
        usage='<theme>'
    )
    async def image(self, ctx, theme):
        
        async with ctx.typing():
            image_url = get_images(1, theme)[0]

            imageEmbed = discord.Embed(
                title=f'Image de {theme} :',
                url=image_url,
                color=self.client.color['AQUA']
            )
            imageEmbed.set_image(url=image_url)

        await ctx.send(embed=imageEmbed)

    @commands.command(
        name='meme',
        description='Renvoie un meme aléatoire tiré de Reddit',
        usage='[nombre] || De base 1 et max 5'
    )
    async def meme(self, ctx, number=1):
        if number >= 5:
            errorEmbed = discord.Embed(
                title='Ca fait beaucoup la non',
                description='Le nombre de meme en même temps est limité à 5.',
                color=self.client.color['RED']
            )
            await ctx.send(embed=errorEmbed)
            return
        
        async with ctx.typing():
            subRedditList = await get_meme(number)
            
            for subReddit in subRedditList:
                redditEmbed = discord.Embed(
                    name=subReddit.title,
                    url=subReddit.url,
                    color=self.client.color['NAVY']
                )

                redditEmbed.set_image(url=subReddit.url)
            
                await ctx.send(embed=redditEmbed)


def setup(client):
    client.add_cog(Meme(client))