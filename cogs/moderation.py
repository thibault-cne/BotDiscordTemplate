"""
    Author : @Vladou
    Discord : Thibô#0001
"""

import discord
from discord.ext import commands

from cogs._coreJson import read_json, write_json
from cogs._corePrefix import get_guild_prefix
from cogs._coreChecks import check_disabledCommands
from cogs._coreModeration import removeUser, searchUser



class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    
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

    
    @commands.command(
        name="blacklist",
        description="Permet de blacklist un compte discord du serveur en l'empêchant de se reconnecter sans avoir a le ban.",
        usage="<@member>"
    )
    @check_disabledCommands()
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
            blackList[guild_id]['BlackListMember'] = [[user_id, ctx.author.id]]
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
            blackList[guild_id]['BlackListMember'].append([user_id, ctx.author.id])
            write_json(blackList, 'blackList')

        await ctx.send(embed=blackListEmbed)
    

    @commands.command(
        name="unblacklist",
        description="Permet de un-blacklist un compte discord du serveur.",
        usage="<@member>"
    )
    @check_disabledCommands()
    async def unblacklist(self, ctx, user):
        blackList = read_json('blackList')

        guild_id = str(ctx.guild.id)
        user_id = str(user)

        blackListEmbed = discord.Embed(
            title='Un-blacklist',
            color=self.client.color['WHITE']
        )

        if guild_id not in blackList or not searchUser(blackList, user_id, guild_id):
            blackListEmbed.description = f"L'utilisateur <@{user}> n'est pas blackliste.\n\
                Vous pouvez consulter la liste des personnes blacklist avec : ```{get_guild_prefix(self.client, guild_id)}blackedmember```\n\
                Vous pouvez le blacklist avec ```{get_guild_prefix(self.client, guild_id)}blacklist```."
        else:
            blackListEmbed.description = f"L'utilisateur <@{user}> à bien été un-blacklist.\n\
                Vous pouvez consulté la liste des personnes blacklist avec ```{get_guild_prefix(self.client, guild_id)}blackedmember```"
            newDict = removeUser(blackList, user_id, guild_id)
            write_json(newDict, 'blackList')

        await ctx.send(embed=blackListEmbed)


    @commands.command(
        name="blackedmember",
        description="Affiche la liste des membres blacklist du discord."
    )
    @check_disabledCommands()
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
            for tuples in blackList[guild_id]["BlackListMember"]:
                blackListStr += f"<@{tuples[0]}> à été blacklist par <@{tuples[1]}>\n"
            blackListEmbed.description = blackListStr

        await ctx.send(embed=blackListEmbed)


def setup(client):
    client.add_cog(Moderation(client))