prefix = '!'
import discord
from discord.ext import commands, tasks
import random
import datetime
from discord.ext.commands.errors import MissingRequiredArgument, CommandNotFound
import os
import json
import wikipedia 
import asyncio
from itertools import cycle
from discord_buttons_plugin import *


token = os.environ['TOKEN']



client = commands.Bot(command_prefix =commands.when_mentioned_or(prefix), case_insensitive = True)
buttons = ButtonsClient(client)

def roll_convert(argument):
    intarg = int(argument)
    switcher = {
        1: "1️⃣",
        2: "2️⃣",
        3: "3️⃣",
        4: "4️⃣",
        5: "5️⃣",
        6: "6️⃣",
        7: "7️⃣",
        8: "8️⃣",
        9: "9️⃣",
        0: "0️⃣"
    }
    return switcher.get(intarg, "what")


status = cycle([
  'Algum jogo',
  'Host: Repl.it',
  'Powered by: General Djarin'
])

@tasks.loop(seconds=10)
async def status_swap():
  await client.change_presence(activity=discord.Game(next(status)))

@client.event
async def on_ready():
  status_swap.start()
  print('Entramos como {0.user}' .format(client))


@client.event
async def on_command_error(ctx, error):
    if isinstance(error,MissingRequiredArgument):
        await ctx.send(':x: | Coloque todos os argumentos!')
    elif isinstance(error,CommandNotFound):
        await ctx.send(':x: | Comando não encontrado!')


@client.command()
async def bola8(ctx, *, pergunta):
  responses = ['Sim', 'Com certeza!', 'Talvez sim', 'talvez', 'não', 'de jeito nenhum', 'Não sei :/', '¯\_(ツ)_/¯', 'Não tenho certeza sobre isso', 'Pergunte novamente']
  await ctx.send(f'Pergunta: {pergunta}\n Resposta: {random.choice(responses)}')

@client.command()
async def say(ctx, *, mensagem):
  await ctx.send(f'{ctx.author} disse: {mensagem}')

@client.command()
async def kick(ctx, membro: discord.Member, *,motivo=None):
  if ctx.author.guild_permissions.kick_members:
    await membro.kick()
    await ctx.send(':oncoming_police_car: | Membro expulso com sucesso!')


@client.command()
async def timer(ctx, seconds):
    try:
        secondint = int(seconds)
      
        if secondint <= 0:
            await ctx.send("Eu não consigo contar com números negativos!")
        
        else:
            message = await ctx.send(f"Timer: {seconds}")
            
            while True:
                secondint -= 1
                if secondint == 0:
                    await message.edit(content="Acabou!")
                    break
                        
                await message.edit(content=f"Timer: {secondint}")
                await asyncio.sleep(1)
    except ValueError:
        await ctx.send('Você precisa colocar um número!')

@client.command()
async def invite(ctx):
	embed = discord.Embed(title=f"Invite", color=0xff0000, description=f'Convite o bot para seu servidor também!')
	await buttons.send(
		content = None,
		embed = embed,
		channel = ctx.channel.id,
		components = [
			ActionRow([
				Button(
					style = ButtonType().Link,
					label = "Invite",
					url = 'https://discord.com/api/oauth2/authorize?client_id=829142257357029376&permissions=8&scope=bot%20applications.commands'
				)
			])
		]
	)

@client.command()
async def weather(ctx, *, message=None):
	embed = discord.Embed(color=123456,
	                      timestamp=ctx.message.created_at,
	                      title=f"tempo em {message}")
	embed.set_image(
	    url=
	    f"https://api.cool-img-api.ml/weather-card?location={message}&background=https://cdn.discordapp.com/attachments/820496743211728937/829268642801647636/2021-04-07-15-17-17.jpg"
	)
	await ctx.send(embed=embed)

@client.command()
async def rev(ctx, *, var):
    stuff = var[::-1]
    embed = discord.Embed(description = stuff)
    embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
    await ctx.send(embed = embed)

@client.command()
async def forca(ctx):
  text= ['discord', 'bot', 'python', 'javascript', 'mandalorian', 'admin', 'adm']
  text=random.choice(text)
  text=text.lower()
  tries=0
  lettersdone=[]
  sendtext=""
  win="false"
  for i in text:
    if i.isspace():
      sendtext=f'{sendtext} '
    else:
      sendtext=f'{sendtext}🟦'
  messageid=await ctx.send(f"**{ctx.author}**, O jogo da forca começou, tem **{len(text)}** letras: `{sendtext}`")
  while tries<6:
    def check(m):
      return m.channel==ctx.channel
    content=await client.wait_for('message', check=check)
    content=content.content.lower()
    if len(content)!=1:
      continue
    else:
      if content in text:
        if content in lettersdone:
          sendlettersdone=", ".join(lettersdone).upper()
          await ctx.send(f"Você acertou`{sendlettersdone}`, e `{content}` estava incluído!")
        else:
          lettersdone.append(content)
          sendtext=list(sendtext)
          for i in range(len(text)):
            if text[i]==content:
              sendtext[i]=content
          sendtext="".join(sendtext)
          sendlettersdone=", ".join(lettersdone).upper()
          if sendtext.replace(text, " ").isspace():
            await messageid.edit(content=f"**__Game Over__**\nTexto final: `{sendtext}`\nLetras que você usou: `{sendlettersdone}`\nChances: `{6-tries}`")
            win="true"
            break
          else:
            await messageid.edit(content=f"Está certo, resultado do jogo: `{sendtext}`\nLetras usadas: `{sendlettersdone}`\nQuantidade de letras que você ainda pode errar: `{6-tries}`")
      else:
        if content in lettersdone:
          sendlettersdone=", ".join(lettersdone).upper()
          await ctx.send(f"Você acertou`{sendlettersdone}`,e `{content}` está incluído nele!")
        else:
          lettersdone.append(content)
          tries=tries+1
          sendlettersdone=", ".join(lettersdone).upper()
          await messageid.edit(content=f"Resultado do jogo: `{sendtext}`\nLetras usadas: `{sendlettersdone}`\nTentativas faltando: `{6-tries}`")
  if win=="true":
    await ctx.send(f"Parabéns! Você conseguiu acertar a palavra **{text}** e com apenas **{tries}** resposta(s) errada(s)!")
  else:
    await ctx.send(f"Você errou, era **{text}**!")

@client.command()
async def userinfo(ctx, *, member: discord.Member = None):
  if member==None:
    member=ctx.author
  roles=[x.mention for x in member.roles]
  roles=", ".join(roles)
  embed = discord.Embed(title="User Info")
  embed.description = """
**Tag completa:** {.name}#{.discriminator}\n
**Nickname:** {.nick}\n
**Data de criação:** {.created_at}\n
**Entrou no servidor:** {.joined_at}\n
**Status:** {.status}\n
**Avatar URL:** [Clique aqui]({.avatar_url})\n
**É um bot:** {.bot}""".format(member, member, member, member, member, member, member, member)
  embed.set_thumbnail(url=member.avatar_url)
  await ctx.send(embed=embed)

@client.command()
async def ship(ctx, membro1: discord.Member, membro2: discord.Member):
  chances = ['0%, não da certo nem nos sonhos!', '5%, as chances são quase 0!', '10%, é... eu acho que não', '20%, talvez', '30%, é possível', '40%, acho que pode acontecer!', '50%, Sim!', '60%, Com certeza!', '70%, se bobear, eles até já estão juntos!', '80%, Nada pode impedir!', '90%, Caraca, acho que já devem até estar casados!', '100%, não preciso nem falar né?']
  embed = discord.Embed(title='Teste de casal', description = f'Usuários: {membro1} e {membro2}\n Resultado: {random.choice(chances)}')
  await ctx.send(embed = embed)

@client.command()
async def ping(ctx):
  a = client.latency
  b = int(a*1000)
  await ctx.send(f':ping_pong: | Pong! Meu ping é: {b}')


@client.command()
async def ban(ctx, membro: discord.Member, *,motivo=None):
  if ctx.author.guild_permissions.ban_members:
    await membro.ban()
    await ctx.send(':oncoming_police_car: | Membro banido com sucesso!')

@client.command()
async def roll(ctx):
    r = str(random.randrange(1, 101))
    mes = 'Seu número (De 1 a 100) - '
    for m in r:
        mes += roll_convert(m)

    await ctx.send(mes)



@client.command()
async def dado(ctx, numero):
  variavel = random.randint(1,int(numero))
  await ctx.send(f'O número que saiu no dado é {variavel}')


@client.command(aliases=['cara', 'coroa'], help='Jogue cara ou coroa!')
async def moeda(ctx):

  var = random.randint(1, 2)
  if var == 1:  # cara
    await ctx.send('Deu cara!')
  elif var == 2:  # coroa
   await ctx.send('Deu coroa!')
  

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

@client.command(aliases=['clean', 'limpar'])
async def clear(ctx, n=0):
  if ctx.author.guild_permissions.manage_messages:
    if n <= 0:
      await ctx.send('Você precisa digitar a quantidade de menssagens para serem deletadas')
    else:
      await ctx.channel.purge(limit=int(n))
      x = discord.Embed(title='Sistema de Limpar!')
      x.add_field(name='Menssagens deletadas:', value=f'{n}')
      x.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
      x.timestamp = datetime.datetime.utcnow()
      msg = await ctx.send(embed=x)
  else:
    await ctx.send(':x: | Você não tem permissão para isso!')

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

@client.command()
async def wiki(ctx, *, arg=None):
    try:
        if arg == None:
            await ctx.send("Coloque o que você quer pesquisar")
        elif arg:
            start = arg.replace(" ", "")
            end = wikipedia.summary(start)
            await ctx.send(end)
    except:
        try:
            start = arg.replace(" ", "")
            end = wikipedia.summary(start, sentences=10)
            await ctx.send(end)
        except:
            await ctx.send(":x: | Ocorreu um erro! 404")


@client.command()
async def ajuda(ctx):
  embed = discord.Embed(
    title = 'Ajuda: Versão python',
    description = '**Comandos:** Por enquanto, na versão python, é só isso:',
    colour = 11598249
  )

  embed.set_author(name='OBS: A não ser o M! do prefixo, os comandos não precisam ter exatamente as maiúsculas, exemplo: M!Ping, M!ping, M!PiNg, etc. vão funcionar!')

  embed.add_field(name='Diversão', value='>>> M!Ping\n M!Dado <número>\n M!Roll\n M!Ship <@usuario1> <@usuario2>\n M!Forca\n M!Bola8 <pergunta>\n M!Say <palavra ou frase>\n M!Weather <cidade>\n M!Wiki <alguma coisa>\n M!Avatar {@usuário}\n M!Moeda\n M!Rev <palavra ou frase>\n M!Timer <segundos>', inline=False)
  embed.add_field(name='Moderação', value='>>> M!Ban <@membro>\n M!Kick <@membro>\n M!Clear <mensagens>\n M!Userinfo {@usuário}\n M!Server\n M!Ping\n M!Invite', inline=True)
  embed.add_field(name='Em breve', value='Em breve', inline=True)

  await ctx.send(embed = embed)

client.run(token)
