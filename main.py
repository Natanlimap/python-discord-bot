import discord
from discord.ext import commands
from discord.utils import get

import json
import os
import time

from PIL import Image
from io import BytesIO

import twitter as Twitter

# Verificar se o arquivo de configuração existe
if os.path.exists(os.getcwd() + "/config.json"):
    
    # Pegar os dados dos arquivo de configuração e de data   
    with open("./config.json") as f:
        configData = json.load(f)
    
#  Caso o arquivo de configuração não exista       
else:

    # criando um arquivo de configuração padrão
    configTemplate = {"Token": "", "Prefix": "-"}

    with open(os.getcwd() + "/config.json", "w+") as f:
        json.dump(configTemplate, f) 


# Passando os parametros do arquivo de configuração
token = configData["Token"]
prefix = configData["Prefix"]


# Criando o intents para poder receber informações privilegiadas do servidor
intents = discord.Intents.default()
intents.members = True 
bot = commands.Bot(command_prefix=prefix, intents=intents)


# Como não será preciso nesse escopo está comentado

# Permite o bot falar com outro
# bot._skip_check = lambda x, y: False

# Permite o bot falar com outro
# @bot.event
# async def on_message(message):
#     ctx = await bot.get_context(message)
#     await bot.invoke(ctx)




# Quando o bot for inicializado
@bot.event
async def on_ready():    
    print("Bot is ready.")



# O bot entra no canal de voz de onde o usuário está
async def joinChannel(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    
    await ctx.send(f'Join {channel}')
    
# O bot sai do canal de voz de onde o usuário está

async def leaveChannel(ctx):
    voice = get(bot.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()


@bot.command()
async def poll(ctx, *, message):
    emb = discord.Embed(tile='VOTAÇÂO', description=f'{message}')
    botMessage = await ctx.channel.send(embed=emb)
    await botMessage.add_reaction('👍')
    await botMessage.add_reaction('👎')

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

@bot.command()
async def twitter(ctx, user, quant):
    print(user)
    menssagens = Twitter.getTweets(user, quant)

    for mensagem in menssagens:
        embedVar = discord.Embed(title=("@" + user), description=(mensagem), color=0x1DE7EB)
        await ctx.send(embed=embedVar)


bot.run(token)