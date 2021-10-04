prefix = '!'
import discord
from discord.ext import commands
import random
import datetime
from discord.ext.commands.errors import MissingRequiredArgument, CommandNotFound
import os
import json

token = os.environ['TOKEN']


client = commands.Bot(command_prefix = prefix, case_insensitive = True)

@client.event
async def on_ready():
  activity = discord.Game(name='Use M!Ajuda ou M!Help para ver os comandos, OBS: Versão Python ativa!', type=3)
  await client.change_presence(status=discord.Status.online, activity=activity)
  print('Entramos como {0.user}' .format(client))


@client.event
async def on_command_error(ctx, error):
    if isinstance(error,MissingRequiredArgument):
        await ctx.send(':x: | Coloque todos os argumentos!')
    elif isinstance(error,CommandNotFound):
        await ctx.send(':x: | Comando não encontrado, se está usando a versão DBD, ignore essa mensagem')

# comando teste, de mandar "oi"
@client.command()
async def ola(ctx):
  await ctx.send(f'Olá, {ctx.author}')

# comando de say, <prefixo>say <frase>
@client.command()
async def say(ctx, mensagem):
  await ctx.send(f'{ctx.author} disse: {mensagem}')

# comando de kick, <prefixo>kick @usuario
@client.command()
async def kick(ctx, membro: discord.Member, *,motivo=None):
  if ctx.author.guild_permissions.kick_members:
    await membro.kick()
    await ctx.send(':oncoming_police_car: | Membro expulso com sucesso!')

# comando de ban, <prefixo>ban @usuario
@client.command()
async def ban(ctx, membro: discord.Member, *,motivo=None):
  if ctx.author.guild_permissions.ban_members:
    await membro.ban()
    await ctx.send(':oncoming_police_car: | Membro banido com sucesso!')

#comando dado, use <prefixo>dado <número>, exemplo: !dado 12
@client.command()
async def dado(ctx, numero):
  variavel = random.randint(1,int(numero))
  await ctx.send(f'O número que saiu no dado é {variavel}')

#comando de cara ou coroa, use <prefixo>moeda 
@client.command(aliases=['cara', 'coroa'], help='Jogue cara ou coroa!')
async def moeda(ctx):

  var = random.randint(1, 2)
  if var == 1:  # cara
    await ctx.send('Deu cara!')
  elif var == 2:  # coroa
   await ctx.send('Deu coroa!')
  
# comando de avatar, use <prefixo>avatar ou <prefixo>avatar @membro, exemplo !avatar ou !avatar @usuário
@client.command(alises=['foto', 'img'])
async def avatar(ctx, membro : discord.Member = 'nada'):
  if membro != 'nada':
    x = discord.Embed(title=f'Avatar de {membro.display_name}')
    x.set_image(url=membro.avatar_url)
    x.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=x)
  else:
    x = discord.Embed(title='Seu avatar')
    x.set_image(url=ctx.author.avatar_url)
    x.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=x)

# comando clear, use <prefixo>clear <número>, exemplo, !clear 10
@client.command(aliases=['clean', 'limpar'])
async def clear(ctx, n=0):
  if n <= 0:
    await ctx.send('Você precisa digitar a quantidade de menssagens para serem deletadas')
  else:
    await ctx.channel.purge(limit=int(n))
    x = discord.Embed(title='Sistema de Limpar!')
    x.add_field(name='Menssagens deletadas:', value=f'{n}')
    x.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    x.timestamp = datetime.datetime.utcnow()
    msg = await ctx.send(embed=x)

# comando de serverinfo: não funcionando
@client.command()
async def server(ctx):
  membros = len(ctx.guild.members)
  cargos = len(ctx.guild.roles)
  x = discord.Embed(title='**Informações:**')
  x.add_field(name='Nome:', value=ctx.guild.name, inline=False)
  x.add_field(name='ID:', value=ctx.guild.id, inline=False)
  x.add_field(name='Dono:', value=ctx.guild.owner.mention, inline=False)
  x.add_field(name='Criado em:', value=ctx.guild.created_at.strftime('Data: %d/%m/%Y Hora: %H:%M:%S %p'), inline=False)
  x.add_field(name='Região:', value=ctx.guild.region, inline=False)
  x.add_field(name='Membros:', value=f'`{membros}`', inline=False)
  x.add_field(name=f'Cargos:', value=f'`{cargos}`', inline=False)
  x.set_thumbnail(url=ctx.guild.icon_url)
  x.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
  x.timestamp = datetime.datetime.utcnow()
  await ctx.send(embed=x)

client.run(token)
