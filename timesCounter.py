import json
import os

async def increase(ctx, counter): 
    await ctx.send(F"This function was called {counter} times")
    configTemplate = {"Times": counter}
    with open(os.getcwd() + "/data.json", "w+") as f:
        json.dump(configTemplate, f) 



async def get(ctx, counter): 
    await ctx.send(F"The counter has already been incremented {counter} times")
  