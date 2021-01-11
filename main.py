import discord
from discord.ext import commands
from discord.utils import get

import json
import os
import ddmais as dd
import timeout as timeoutfile
import time

# verificar se o arquivo de configuração existe
if os.path.exists(os.getcwd() + "/config.json"):
    
    with open("./config.json") as f:
        configData = json.load(f)
    
    with open("./ddmais.json") as ddmaisJson:
        configDataDDMais = json.load(ddmaisJson)

else:
    # criando um arquivo de configuração padrão
    configTemplate = {"Token": "", "Prefix": "["}

    with open(os.getcwd() + "/config.json", "w+") as f:
        json.dump(configTemplate, f) 

# passando os parametros do arquivo de configuração
token = configData["Token"]
prefix = configData["Prefix"]
flanasCounter = configDataDDMais["Flanas"]


intents = discord.Intents.default()
intents.members = True 
bot = commands.Bot(command_prefix=prefix, intents=intents)

@bot.event
async def on_ready():    
    print("Bot is ready.")

@bot.command()
async def flanas(ctx):
    global flanasCounter
    flanasCounter = flanasCounter + 1
    await dd.flanas(ctx, flanasCounter)


@bot.command()
async def bolha(ctx):
    await dd.bolha(ctx)



@bot.command()
async def timeout(ctx, member: discord.Member):
    await timeoutfile.timeout(ctx, member)

@bot.command()
async def vote(ctx):
    await timeoutfile.vote(ctx)

@bot.command()
async def teste(ctx):
    vc = ctx.message.author.voice.channel.id
    print(vc)


@bot.command()
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    
    await ctx.send(f'Entrou em {channel}')
    
@bot.command()
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()


bot.run(token)