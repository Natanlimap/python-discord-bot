import twint
import nest_asyncio
import pandas as pd;
import os
nest_asyncio.apply()


def getTweets(user, quant):
    mensages = []
    c = twint.Config()
    c.Username = user
    c.Limit = 5
    c.Store_csv = True
    c.Output = user + ".csv"
    c.Lang = "pt"
    twint.run.Search(c)
    df = pd.read_csv(user + ".csv", nrows=int(quant) )
    for index, row in df.iterrows():
        mensages.append(row['tweet'])
        print(row['tweet'])
    os.remove(user + ".csv")

    return mensages