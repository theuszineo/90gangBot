import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import datetime

client = commands.Bot(command_prefix = '/')

#my discord server: https://discord.gg/HSC4srX
@client.event
async def on_ready():
    print('bot online!')


@client.command()
async def ajuda(ctx):
    await ctx.channel.purge(limit=1)
    await ctx.send('''```\nCommands list:
    /ping, Show you ping in ms.
    /envite, Public Envite for a guild.
    /clear amount, delete messages - ONLY ADMINISTRATOR.
    /kick @member <reason>, kick members from serve - ONLY WITH KICK PERMISSION.
    /ban @member <reason>, Ban members from serve - ONLY WITH BAN PERMISSION.
    /unban nome#tag, Unban banned menbers, ONLY WITH BAN PERMISSION.```''')


@client.command()
async def ping(ctx):
    await ctx.channel.purge(limit=1)
    await ctx.send(f'```ping: {round(client.latency * 1000)}ms```')


@client.command()
@commands.has_role('owner')
async def envite(ctx):
    await ctx.channel.purge(limit=1)
    embed = discord.Embed(title="envite", colour=discord.Colour(0x75bc48), url="https://discord.gg/HSC4srX", description="Invite your friends. ```\n https://discord.gg/HSC4srX```", timestamp=datetime.datetime.utcfromtimestamp(1589671517))

    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_author(name=f"{ctx.message.author}", url="https://discordapp.com", icon_url=ctx.guild.icon_url)
    embed.set_footer(text="footer text", icon_url=ctx.guild.icon_url)

    embed.add_field(name="everyone can use", value="CALL YOU ..")

    await ctx.send(embed=embed)


@client.command()
@commands.has_role('administrator')
async def clear(ctx, amount=6):
    await ctx.channel.purge(limit=amount)


@client.command()
@has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member, *, reason=None):
    await ctx.channel.purge(limit=1)
    await ctx.send(f'```diff\n-membro: {user}, has Kicked\nReason: <{reason}>. by @{ctx.message.author}```')
    await user.kick(reason=reason)


@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member, *, reason=None):
    await ctx.channel.purge(limit=1)
    await ctx.send(f'```diff\n-member: {user}, has Banned\nReason: <{reason}>. by @{ctx.message.author}```')
    await user.ban(reason=reason)


@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entrys in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'unbanned {user.name}#{user.discriminator}')


@client.command()
@commands.has_role('owner')
async def stop(ctx):
	await ctx.channel.purge(limit=1)
	await ctx.send('```\nturning off the bot```')
	quit()


client.run('token')
