import discord
import os
import rule


rules = None
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await rules.handle(message)


def start_client():
    global rules
    token = read_token('.token')
    rules = read_rules()
    client.run(token)


def read_token(path):
    if not os.path.isfile(path):
        raise ValueError(f'No such file: {path}')
    with open(path, 'r') as f:
        return f.read()


def read_rules():
    return rule.Rules('rules.json')


if __name__ == '__main__':
    start_client()
