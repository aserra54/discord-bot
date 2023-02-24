import configparser
import discord
import os
import random


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


async def send(channel, lines, percentage):
    if len(lines) == 0:
        return
    if random.random() < percentage:
        selected_line = random.choice(lines)
        await channel.send(selected_line)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.channel.name == 'deep-rock-galactic':
        await handle_deep_rock_galactic_message(message)
    elif message.channel.name == 'phasmophobia':
        await handle_phasmophobia(message)


async def handle_deep_rock_galactic_message(message):
    lines = []
    percentage = 1
    if 'rock and stone' in message.content.lower():
        lines = ['Rock and stone!', 'For rock and stone!', 'ROCK... AND... STONE!', 'Rock and stone forever!', 'That\'s it lads, rock and stone!']
    elif 'for karl' in message.content.lower():
        lines = ['For Karl!']
    elif 'karl' in message.content.lower() and 'karl.gg' not in message.content.lower():
        lines = ['I miss Karl.']
        percentage = 0.10
    elif message.author.name == 'tattlebag':
        lines = ['Careful with the C4 there.', 'Did you drop your C4 again?']
        percentage = 0.05
    await send(message.channel, lines, percentage)


async def handle_phasmophobia(message):
    lines = []
    percentage = 1
    if message.author.name == 'DVR':
        lines = ['I see you waiting in the van, Daniel.', 'Go wait in the van, Daniel.']
        percentage = 0.05
    await send(message.channel, lines, percentage)


def start_client():
    if not os.path.isfile('config.ini'):
        raise Exception('Could not find configuration file')
    config = configparser.ConfigParser()
    config.read('config.ini')
    token = config['BOT']['token']
    client.run(token)


if __name__ == '__main__':
    start_client()
