import json
import os

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

# Chat bot config
chatbot = ChatBot(
    'PythonBot',
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

# Funçao que envia para o discord uma mensagem respondendo a mensagem enviada pelo usuário
async def message(ctx, msg):
    response = chatbot.get_response(msg)
    await ctx.send(F"{response}")
