import discord
from discord.ext import commands
import json
import os
import ddmais as dd
import timeout as timeoutfile


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

bot = commands.Bot(command_prefix=prefix)

@bot.event
async def on_ready():    
    print("Bot is ready.")

@bot.command()
async def flanas(ctx):
    global flanasCounter
    flanasCounter = flanasCounter + 1
    await dd.flanas(ctx, flanasCounter)

@bot.command()
async def timeout(ctx, member: discord.Member):
    await timeoutfile.timeout(ctx, member)

@bot.command()
async def vote(ctx):
    await timeoutfile.vote(ctx)

bot.run(token)