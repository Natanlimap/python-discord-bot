import discord
from discord.ext import commands
from discord.utils import get
import asyncio 
import math


memberSelected = None
userThatvoted = []
voteCounter = 0

async def timeout(ctx, member):
    global memberSelected
    memberSelected = member
    await ctx.send(F"The vote to silence {memberSelected.mention}  for 10 minutes will start soon. Type -vote if you agree")

    # PEGANDO A QUANTIDADE DE USUARIOS LOGADOS
    minAmountTimeOut = usersAmount(ctx)

    await ctx.send(F"{voteCounter}/{minAmountTimeOut}")

    

async def vote(ctx):
    global memberSelected
    global userThatvoted
    global voteCounter

    author = ctx.message.author
    for users in userThatvoted:
        if(users == author):
            await ctx.send(F"Im sorry but you can only vote once")

            return

    userThatvoted.append(author)

    # CASO O TIMEOUT NAO TENHA SIDO INICIADO 
    if memberSelected is None:
        await ctx.send(f"type -timeout @user to start a vote")
        return        


    # PEGANDO A QUANTIDADE DE USUARIOS LOGADOS
    minAmountTimeOut = usersAmount(ctx)

    # CASO NÃO TENHA CHEGADO AINDA NA QUANTIDADE MINIMA DE VOTAÇÃO
    if(voteCounter < minAmountTimeOut):
        voteCounter += 1
        await ctx.send(F"{voteCounter}/{minAmountTimeOut}")

    # QUANDO ATINGIR A QUANTIDADE MINIMA
    if(voteCounter == minAmountTimeOut):        
        await ctx.send(F"{memberSelected.mention} has been mutated for 10 minutes")
        await mute(ctx)
        resetVoteMemberUser()


async def mute(ctx):
    mutedTimeInSeconds = 100000 
    await memberSelected.edit(mute=True)
    await asyncio.sleep(mutedTimeInSeconds)
    await unMute()

async def unMute():
     await memberSelected.edit(mute=False)


# PEGANDO A QUANTIDADE DE USUARIOS LOGADOS
def usersAmount(ctx):
    
    voiceChannelID = ctx.message.author.voice.channel.id
    voiceChannel = discord.utils.get(ctx.guild.channels, id=voiceChannelID)
    voiceChannelUsersAmount = round(len(voiceChannel.members)*0.7)
    minAmountTimeOut = voiceChannelUsersAmount
    if (minAmountTimeOut == 0):
        minAmountTimeOut = 1
    return minAmountTimeOut


def resetVoteMemberUser():
    global memberSelected
    global userThatvoted
    global voteCounter
    voteCounter = 0
    memberSelected = None
    userThatvoted = []
    
