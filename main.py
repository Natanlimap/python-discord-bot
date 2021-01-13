import discord
from discord.ext import commands
from discord.utils import get

import json
import os
import timesCounter as TimesCounterFile
import timeout as timeoutfile
import time

from PIL import Image
from io import BytesIO


import mychatbot as chat

# Verificar se o arquivo de configuração existe
if os.path.exists(os.getcwd() + "/config.json"):
    
    # Pegar os dados dos arquivo de configuração e de data   
    with open("./config.json") as f:
        configData = json.load(f)
    
    with open("./data.json") as dataJson:
        jsonData = json.load(dataJson)

#  Caso o arquivo de configuração não exista       
else:

    # criando um arquivo de configuração padrão
    configTemplate = {"Token": "", "Prefix": "-"}

    with open(os.getcwd() + "/config.json", "w+") as f:
        json.dump(configTemplate, f) 


# Passando os parametros do arquivo de configuração
token = configData["Token"]
prefix = configData["Prefix"]
timesCounter = jsonData["Times"]


# Criando o intents para poder receber informações privilegiadas do servidor
intents = discord.Intents.default()
intents.members = True 
bot = commands.Bot(command_prefix=prefix, intents=intents)


# Quando o bot for inicializado
@bot.event
async def on_ready():    
    print("Bot is ready.")


# Função de mensagem com o chat bot trainável
@bot.command()
async def m(ctx, message):
    await chat.message(ctx, message)


# Incrementa o contador
@bot.command()
async def increaseTimesCounter(ctx):
    global timesCounter
    timesCounter = timesCounter + 1
    await TimesCounterFile.increase(ctx, timesCounter)


# Pega o valor do contador
@bot.command()
async def getTimesCounter(ctx):
    await TimesCounterFile.get(ctx, timesCounter)


# Função de timeout para um usuário
@bot.command()
async def timeout(ctx, member: discord.Member):
    await timeoutfile.timeout(ctx, member)

# Votação para o timeout
@bot.command()
async def vote(ctx):
    await timeoutfile.vote(ctx)


# O bot entra no canal de voz de onde o usuário está
@bot.command()
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    
    await ctx.send(f'Join {channel}')
    
# O bot sai do canal de voz de onde o usuário está

@bot.command()
async def leave(ctx):
    voice = get(bot.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()


@bot.command()
async def poll(ctx, *, message):
    emb = discord.Embed(tile='VOTAÇÂO', description=f'{message}')
    msg = await ctx.channel.send(embed=emb)
    await msg.add_reaction('👍')
    await msg.add_reaction('👎')

@bot.command()
async def wanted(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author 

    wanted = Image.open("wanted.jpg")
    asset = ctx.author.avatar_url_as(size = 128)
    data = BytesIO(await asset.read())
    profilePic= Image.open(data)

    profilePic = profilePic.resize((600, 450))
    wanted.paste(profilePic, (50, 212))

    wanted.save('profile.jpg')

    await ctx.send(file = discord.File('profile.jpg'))
    print(ctx.author)

bot.run(token)