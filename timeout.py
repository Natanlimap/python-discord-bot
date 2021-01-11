import discord
from discord.ext import commands
from discord.utils import get
import asyncio 
import math

global voteCounter
global memberSelected
memberSelected = None

voteCounter = 0

async def timeout(ctx, member):
    global memberSelected
    memberSelected = member
    await ctx.send(F"A DEMOCRACIA VAI VENCER DESSA VEZ")

    voiceChannelID = ctx.message.author.voice.channel.id
    voiceChannel = discord.utils.get(ctx.guild.channels, id=voiceChannelID)
    voiceChannelUsersAmount = len(voiceChannel.members)
    minAmountTimeOut = voiceChannelUsersAmount

    await ctx.send(F"{voteCounter}/{minAmountTimeOut}")

    

async def vote(ctx):
    global memberSelected

    if memberSelected is None:
        await ctx.send(f"Digite [timeout @nome para iniciar a votação")
        return        

    global voteCounter

    voiceChannelID = ctx.message.author.voice.channel.id
    voiceChannel = discord.utils.get(ctx.guild.channels, id=voiceChannelID)
    voiceChannelUsersAmount = len(voiceChannel.members)
    minAmountTimeOut = voiceChannelUsersAmount

    if(voteCounter < minAmountTimeOut):
        voteCounter += 1
        await ctx.send(F"{voteCounter}/{minAmountTimeOut}")

    if(voteCounter == minAmountTimeOut):        
        await ctx.send(F"{memberSelected.mention} teremos paz por 10 minutos")
        await mute(ctx)
        voteCounter = 0
        memberSelected = None

async def mute(ctx):
    await memberSelected.edit(mute=True)
    await asyncio.sleep(4)
    await unMute()

async def unMute():
     await memberSelected.edit(mute=False)


    
