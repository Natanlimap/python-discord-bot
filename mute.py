import discord
from discord.ext import commands

import json
import os


# verificar se o arquivo de configuração existe
if os.path.exists(os.getcwd() + "/config.json"):
    
    with open("./config.json") as f:
        configData = json.load(f)

else:
    # criando um arquivo de configuração padrão
    configTemplate = {"Token": "", "Prefix": "["}

    with open(os.getcwd() + "/config.json", "w+") as f:
        json.dump(configTemplate, f) 

# passando os parametros do arquivo de configuração
token = configData["Token"]
prefix = configData["Prefix"]

bot = commands.Bot(command_prefix=prefix)

@bot.event
async def on_ready():
    print("Bot is ready.")



bot.run(token)