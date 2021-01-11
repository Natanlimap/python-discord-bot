import discord
from discord.ext import commands
import asyncio

global voteCounter
global memberSelected
memberSelected = None

voteCounter = 0

async def timeout(ctx, teste):
    global memberSelected
    memberSelected = teste
    await ctx.send(F"A DEMOCRACIA VAI VENCER DESSA VEZ")
    await vote(ctx)
    
    

async def vote(ctx):
    global memberSelected

    if memberSelected is None:
        await ctx.send(f"Digite [timeout @nome para iniciar a votação")
        return        

    global voteCounter

    minAmountTimeOut = 2

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


    
