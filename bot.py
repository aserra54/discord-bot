import configparser
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
    if not os.path.isfile('config.ini'):
        raise Exception('Could not find configuration file')
    config = configparser.ConfigParser()
    config.read('config.ini')
    token = config['BOT']['token']
    rules = read_rules()
    client.run(token)


def read_rules():
    return rule.Rules('rules.ini')


if __name__ == '__main__':
    start_client()
