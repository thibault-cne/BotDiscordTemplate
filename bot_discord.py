"""
    Author : @Vladou
    Discord : Thibô#0001
"""

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv, find_dotenv

from cogs._corePrefix import get_prefix


dotenv_file = find_dotenv()
load_dotenv(dotenv_file)
TOKEN = os.getenv('BOT_TOKEN')

client = commands.Bot(command_prefix=get_prefix, case_insensitive=True)
client.remove_command('help')

#initialisation de chose utile dans le client

client.defaultPrefix = "!"
client.color={
    "WHITE": 0xFFFFFF,
    "AQUA": 0x1ABC9C,
    "GREEN": 0x2ECC71,
    "BLUE": 0x3498DB,
    "PURPLE": 0x9B59B6,
    "LUMINOUS_VIVID_PINK": 0xE91E63,
    "GOLD": 0xF1C40F,
    "ORANGE": 0xE67E22,
    "RED": 0xE74C3C,
    "NAVY": 0x34495E,
    "DARK_AQUA": 0x11806A,
    "DARK_GREEN": 0x1F8B4C,
    "DARK_BLUE": 0x206694,
    "DARK_PURPLE": 0x71368A,
    "DARK_VIVID_PINK": 0xAD1457,
    "DARK_GOLD": 0xC27C0E,
    "DARK_ORANGE": 0xA84300,
    "DARK_RED": 0x992D22,
    "DARK_NAVY": 0x2C3E50,
}


@client.event
async def on_ready():
    print(f'{client.user} est connecté !')
    game = discord.Game("Le meilleur bot du monde !")
    await client.change_presence(activity=game)


if __name__ == "__main__":
    for filename in os.listdir("./cogs"):
        if filename.startswith("_"):
            continue
        elif filename.endswith(".py"):
            client.load_extension(f"cogs.{filename[:-3]}")
            print(f"Cogs {filename[:-3]} has been loaded \n -----")

    client.run(TOKEN)
