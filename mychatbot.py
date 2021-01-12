import json
import os

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer


conversas = "oi galado.oi"
chatbot = ChatBot(
    'BotDaLaje',
    storage_adapter = 'chatterbot.storage.SQLStorageAdapter',
    logic_adapters = [
        'chatterbot.logic.TimeLogicAdapter',
        'chatterbot.logic.BestMatch',
    ],
    database = 'database.sqlite3',
    read_only = False
)



chatbot = ChatBot('Ron Obvious')
trainer = ChatterBotCorpusTrainer(chatbot)


async def message(ctx, msg):
    resposta = chatbot.get_response(msg)
    await ctx.send(F"{resposta}")
    trainer.export_for_training('./my_export.json')


