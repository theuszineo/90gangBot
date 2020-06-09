import discord
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions
from itertools import cycle
import datetime

#prefixo de comando.
client = commands.Bot(command_prefix = '/90')
#remover o comando help padrão do bot.
client.remove_command('help')
#criar um ciclo de status para o que o bot esta jogando.
status = cycle(['para obter ajuda: /90ajuda', 'Inscrever-se:\nwww.youtube.com/c/xcgamer', 'convide seus amigos para o servidor'])

#https://discord.gg/HSC4srX
#https://discord.com/api/oauth2/authorize?client_id=415332587645698050&permissions=805306055&scope=bot
#https://discord.com/api/oauth2/authorize?client_id=415332587645698050&permissions=8&scope=bot
@client.event
async def on_ready():
    mudar_status.start()
    print('bot online!')

#envia o error para o chat.
@client.event
async def on_command_error(ctx, error):
    if str(error) == 'user is a required argument that is missing.':
        await ctx.channel.send('você não marcou o usuario use:\n comando @nome...')
    else:
        await ctx.send(error)

#loop de 10 segundos para trocar o que o bot esta jogando.
@tasks.loop(seconds=10)
async def mudar_status():
    await client.change_presence(activity=discord.Game(next(status)))

#comando de ajuda com comandos, caso trocar o prefixo mude aqui pros usuarios saberem usar.
@client.command(aliases=['help'])
async def ajuda(ctx):
    await ctx.channel.purge(limit=1)
    embed = discord.Embed(title="/90ajuda",
    colour=discord.Colour(0xb185),
    description="""ajudas:
```\n Comandos usuário:
- /90ajuda, Exibe a ajuda com comandos.
- /90ping, Exibe a velocidade de sua conexão em Ms.
- /90userinfo @usuário, Exibe algumas irformações sobre o usuario marcado.
- /90creditos, Exibe um texto com o informações sobre mim e sobre meu criador.
 Comandos moderacão:
- /90limpar quantidade, ira limpar as mensagens anteriores de acordo com o definido, quantidade padrão (5), necessita que o author tenha de permissão de Gerenciar mensagens.
- /90expulsar @membro razão, expulsara o membro marcado pela razão escrita, necessita que o author tenha de permissão de Expulsar membros.
- /90banir @membro razão, ira banir o membro marcado pela razão escrita, necessita que o author tenha de permissão de Banir membros.
- /90desbanir nome#0000, ira desbanir a pessoa que for colocado o nome e o # dela, necessita que o author tenha de permissão de Banir membros.
- /90renomear nome, ira renomear o nome do canal atual para o nome que você escrever, necessita que o author tenha de permissão de Gerenciar canais.
- /90topico topico, ira por o topico que escrever, necessita que o author tenha de permissão de Gerenciar canais.
- /90lento 0 a 21600, ira por o modo chat lento no canal com o tempod de escrita sendo o valor em segundos que você inserir, necessita que o author tenha de permissão de Gerenciar canais.```""")

    embed.set_thumbnail(url=f"{ctx.guild.icon_url}")

    await ctx.send(embed=embed)


#Exibe a velocidade de sua conexão em Ms.
@client.command()
async def ping(ctx):
    await ctx.channel.purge(limit=1)
    await ctx.send(f'```ping: {round(client.latency * 1000)}ms```')

#userinfo @usuário, Exibe algumas irformações sobre o usuario marcado.
@client.command(aliases=['userinfo', 'user-info'])
async def user_info(ctx, user: discord.Member):
    await ctx.channel.purge(limit=1)
    boost = user.premium_since
    perm = discord.Permissions(permissions=user.guild_permissions.value) #pega o valor das permissions
    permissoes = ''
    ustatus = ''
    moderador = False
    administrador = False
    if ctx.guild.owner.id == user.id:
        ustatus += 'dono do servidor\n'
    if perm.administrator:
        permissoes += 'administrador'
        administrador = True #permite o status de administrador
        moderador = True #permite o status de moderador
    else:
        if perm.create_instant_invite:
            permissoes += 'criar convites\n'
        if perm.kick_members:
            permissoes += 'expulsar\n'
            moderador = True
        if perm.ban_members:
            permissoes += 'banir\n'
            moderador = True
        if perm.manage_channels:
            permissoes += 'gerenciar canais\n'
            moderador = True
        if perm.manage_messages:
            permissoes += 'gerenciar mensagens\n'
            moderador = True
        if perm.manage_guild:
            permissoes += 'gerenciar servidor\n'
            moderador = True
            administrador = True
        if perm.add_reactions:
            permissoes += 'adicionar reações\n'
        if perm.view_audit_log:
            permissoes += 'visualizar log de auditoria\n'
        if perm.attach_files:
            permissoes += 'adicionar arquivos\n'
        if perm.view_guild_insights:
            permissoes += 'ver informações da guilda\n'
        if perm.mute_members:
            permissoes += 'mutar membros\n'
            moderador = True
        if perm.deafen_members:
            permissoes += 'ensurdecer membros\n'
            moderador = True
        if perm.move_members:
            permissoes += 'mover membros\n'
            moderador = True
        if perm.manage_nicknames:
            permissoes += 'gerenciar apilidos\n'
            moderador = True
        if perm.manage_roles:
            permissoes += 'gerenciar cargos\n'
            moderador = True
        if perm.manage_emojis:
            permissoes += 'gerenciar emojis\n'
    if moderador:
        ustatus += 'moderador do server\n'
    if administrador:
        ustatus += 'admin do servidor\n'
    if True:
        ustatus += 'normal\n'

    if str(boost) == 'None':
        boost = 'sem boost'
    embed = discord.Embed(colour=discord.Colour(0x1))

    embed.set_author(name=f"{client.user.name}", icon_url=f"{client.user.avatar_url}")
    embed.set_footer(text=f"Pedido por: {ctx.author} | {ctx.author.id}", icon_url=f"{ctx.author.avatar_url}")
    embed.set_thumbnail(url=user.avatar_url)

    embed.add_field(name=f"**informações de\n{user}**",
    value=f"**nome**\n_{user.name}_\n**descriminador**\n_{user.discriminator}_\n**id**\n{user.id}", inline=True)
    embed.add_field(name="**permissões**", value=f"{permissoes}", inline=True)
    embed.add_field(name="**Status do usuário**", value=f"{ustatus}", inline=True)
    embed.add_field(name="**entrou no servidor**", value=f"{user.joined_at}", inline=True)
    embed.add_field(name="**boost desde**", value=f"{boost}", inline=True)

    await ctx.send(content=f"{ctx.author.mention}", embed=embed)

 

#esse e o credito do codigo caso queira dar alguma divulgação para mim.
@client.command()
async def creditos(ctx):
    await ctx.channel.purge(limit=1)
    author = ctx.author
    embed = discord.Embed(title="**credits**",
     colour=discord.Colour(0xff001d), url="http://www.youtube.com/c/xcgamer",
     description="Bot creator: xc_#5273 [Youtube Channel](http://www.youtube.com/c/xcgamer). ```\nhttps://discord.gg/HSC4srX```")

    embed.set_image(url=f"{ctx.guild.icon_url}")
    embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/0raSjpLh6iYeQKOWM2AzRmkYYqL7xvKPj_BgCuXD9nY/https/images-ext-2.discordapp.net/external/OZf53WDoLExvu5l4Oibj4b-WuX2c0MkPtpnbYBuAB3s/%253Fsize%253D1024/https/cdn.discordapp.com/avatars/330869551577300992/55334e62f3b7a98c62d3b1fcc637ea02.webp?width=300&height=300")
    embed.set_author(name=f"{ctx.author}",
    icon_url=f"{author.avatar_url}")
    embed.set_footer(text="signed by xc_ (xc_#5273)",
    icon_url=f"{author.avatar_url}")

    embed.add_field(name="use in your serve too",
    value="[Bot envite](https://discord.com/api/oauth2/authorize?client_id=415332587645698050&permissions=1878523767&scope=bot)",
    inline=True)

    await ctx.send(embed=embed)

comando para limpar chat reservado apenás pra quem tem a permissão de gerenciar mensagens, limpar quantidade.
@client.command()
@commands.has_permissions(manage_messages=True)
async def limpar(ctx, amount=6):
    await ctx.channel.purge(limit=amount)


#comando para expulsar usuarios reservado apenás pra quem tem a permissão de expulsar membros
@client.command()
@has_permissions(kick_members=True)
async def expulsar(ctx, user: discord.Member, *, reason=None):
    await ctx.channel.purge(limit=1)
    await ctx.send(f'```diff\n-membro: {user}, foi Kickado\n Razão: <{reason}>. by @{ctx.message.author}```')
    await user.kick(reason=reason)


#comando para banir usuarios reservado apenás pra quem tem a permissão de banir membros, banir @membro razão.
@client.command()
@commands.has_permissions(ban_members=True)
async def banir(ctx, user: discord.Member, *, reason=None):
    await ctx.channel.purge(limit=1)
    await ctx.send(f'```diff\n-membro: {user}, foi Banido\n Razão: <{reason}>. by @{ctx.message.author}```')
    await user.ban(reason=reason)


@client.command()
@commands.has_permissions(ban_members=True)
async def desbanir(ctx, *, member):
    usuario_banido = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for banido in usuario_banido:
        user = banido.  user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'unbanned {user.name}#{user.discriminator}')    


#esse comando altera o nome do canal
@client.command()
@commands.has_permissions(manage_channels=True)
async def renomear(ctx, *,nome:str):
    nome = nome.replace(' ', '-')
    await ctx.send(f'```diff\nlembrando que o bot necessita de permissão para executar esse processo\n-tentando: trocando o nome do canal para: {nome}\n```\n**processando...**')
    await ctx.send('__pode demorar um pouco as vezes__')
    await ctx.channel.edit(name=nome, reason=f'nome editado a pedido de {ctx.author}')
    await ctx.send(f'pronto! nome trocado para: {nome}')


#esse comando altera o topico do canal
@client.command()
@commands.has_permissions(manage_channels=True)
async def topico(ctx, *, topico:str):
    await ctx.send(f'```diff\nlembrando que o bot necessita de permissão para executar esse processo\n-tentando: trocando o topico do canal para:\n\n{topico}\n```\n**processando...**')
    await ctx.send('__pode demorar um pouco as vezes__')
    await ctx.channel.edit(topic=topico, reason=f'topico editado a pedido de {ctx.author}')
    await ctx.send(f'pronto! topico trocado para:\n{topico}\n```Concluido.```')


#esse comando altera o tempo para falar caso esteja 0 sera desativado para quem tem a permissao de gerenciar mensagens
@client.command()
@commands.has_permissions(manage_channels=True)
async def lento(ctx, tempo=0):
    tempo = int(tempo)
    await ctx.channel.edit(slowmode_delay=tempo)
    if tempo == 0:
        await ctx.send(f'Modo chat lento desativado!')
    else:
        await ctx.send(f'Modo chat lento com tempo de {tempo}!')


#isso e para o dono do bot escrever como o bot no chat
@client.command()
@commands.is_owner()
async def diga(ctx, *, msg):
    await ctx.channel.purge(limit=1)
    await ctx.send(msg)



client.run('seutoken')
