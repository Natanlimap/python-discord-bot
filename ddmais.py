import json
import os

async def flanas(ctx, flanasCounter): 
    await ctx.send(F"Flanas ja afundou {flanasCounter} jogos desde a minha chegada no servidor")
    configTemplate = {"Flanas": flanasCounter}
    with open(os.getcwd() + "/ddmais.json", "w+") as f:
        json.dump(configTemplate, f) 



async def bolha(ctx): 
    await ctx.send(F"Somos contra essa organização criminosa! Somos contra a bolha!")
    for i in range(5):
        await ctx.send(F"FVCK BOLHA")
  