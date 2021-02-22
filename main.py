try:
    import setEnv
except:
    pass

import discord
from discord.ext import commands
from discord.utils import get

import json
import os
import time

from PIL import Image
from io import BytesIO

from utils import getRGBFormat
from MyWeather import getWeather, getIconUrl

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
# token = configData["Token"]
prefix = '-'
token = os.getenv("DISCORD_BOT_TOKEN")
# prefix = os.getenv("DISCORD_BOT_TOKEN")


# Criando o intents para poder receber informações privilegiadas do servidor
intents = discord.Intents.default()
intents.members = True 
bot = commands.Bot(command_prefix=prefix, intents=intents)


ON_JOIN_ROLE_ID = 0

bot.remove_command('help')

# Quando o bot for inicializado
@bot.event
async def on_ready():    
    print("Bot is ready.")


@bot.event
async def on_message(message):
    print(message.content)
    await bot.process_commands(message)
    if(message.content[0] == "-"):
        await message.delete()

# O bot entra no canal de voz de onde o usuário está
@bot.event
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

@bot.command()
async def weather(ctx, local):
    weather = getWeather(local)
    weatherTitle = f'{weather.city} | {weather.region} | {weather.country}'
    weatherDescription = f'Min: {weather.forecast.mintemp} Max: {weather.forecast.maxtemp} \n {weather.forecast.condition}'

    embedVar = discord.Embed(title=weatherTitle, description= weatherDescription,color=0x1DE7EB,)
    embedVar.set_thumbnail(url=getIconUrl(weather.forecast.condition))
    await ctx.send(embed=embedVar)


@bot.command()
async def cdrole(ctx, *, roleName):
    guild = ctx.message.guild
    role = await guild.create_role(name=roleName, hoist=True)
    await ctx.send(f"Cargo {roleName} criado!")

@bot.command()
async def crgbrole(ctx, r, g, b, *, roleName):
    
    guild = ctx.message.guild
    role = await guild.create_role(name=roleName, hoist=True, color=discord.Colour.from_rgb(r=int(r), g=int(g), b=int(b)))
    await ctx.send(f"Cargo {roleName} criado!")


@bot.command()
async def urole(ctx, member:discord.Member, role: discord.Role): 
    if role in member.roles:
        await member.remove_roles(role)
        await ctx.send(f"{member.mention} foi removido ao cargo de {role}")

    else:
        await member.add_roles(role)
        await ctx.send(f"{member.mention} foi adicionado ao cargo de {role}!")
        print(role.id)

@bot.command()
async def setOnJoinRole(ctx, role: discord.Role):
    global ON_JOIN_ROLE_ID
    ON_JOIN_ROLE_ID = role.id
    await ctx.send(f"Role {role} foi definido como o cargo para novos membros")

@bot.command()
async def help(ctx):
    embed=discord.Embed(title=":page_with_curl: Comandos do Hokage", color=0x00b3ff)
    embed.set_author(name=" Hokage help ")
    embed.add_field(name=":white_medium_square: -cdrole [@nome do cargo]", value="Esse comando cria um cargo com o nome desejado.\nExemplo: -cdrole @cargo", inline=False)
    embed.add_field(name=" :rainbow: -crgbrole [ r ] [ g ][ b ] [@nome do cargo]", value="Esse comando cria um cargo com o nome e cor (RGB) desejados.\nExemplo: -crgbrole 0 0 0 @cargo", inline=False)
    embed.add_field(name="-setOnJoinRole [@nome do cargo]", value="Esse comando define o cargo padrão dos novos usuários.\nExemplo: -setOnJoinRole @cargo", inline=False)
    embed.add_field(name="-urole [@user] [@nome do cargo]", value="Esse comando adicionar ou remove o usuário do cargo desejado.\nExemplo: -urole @user @cargo", inline=False)
    embed.add_field(name=":white_sun_rain_cloud: -weather [nome da cidade]", value="Esse comando mostra a previsão do tempo da cidade desejada.\nExemplo: -weather Natal", inline=False)
    embed.set_footer(text="Obrigado por utilizar o bot Hokage :pray: ")
    await ctx.send(embed=embed)

#eventos

@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, id=ON_JOIN_ROLE_ID)
    await member.add_rles(role)




bot.run(token)


