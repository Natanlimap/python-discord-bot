import discord
from discord.ext import commands
from discord.utils import get

import json
import os
import timesCounter as TimesCounterFile
import timeout as timeoutfile
import time


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



@bot.command()
async def m(ctx, message):
    await chat.message(ctx, message)

@bot.command()
async def increaseTimesCounter(ctx):
    global timesCounter
    timesCounter = timesCounter + 1
    await TimesCounterFile.increase(ctx, timesCounter)


@bot.command()
async def getTimesCounter(ctx):
    await TimesCounterFile.get(ctx, timesCounter)



@bot.command()
async def timeout(ctx, member: discord.Member):
    await timeoutfile.timeout(ctx, member)

@bot.command()
async def vote(ctx):
    await timeoutfile.vote(ctx)



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
    
@bot.command()
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()


bot.run(token)