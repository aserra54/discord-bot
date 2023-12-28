import app
import disnake
import os


# setup the bot globally
INTENTS = disnake.Intents.default()
INTENTS.message_content = True
bot = disnake.ext.commands.Bot(intents=INTENTS, command_prefix='!')
app = app.App()


@bot.event
async def on_ready():
    app.initialize(bot, 'data/msg-rules.json')


@bot.event
async def on_message(message):
    await app.message_handler.handle(bot, message)


def read_token(token_path):
    if not os.path.isfile(token_path):
        raise ValueError(f'No such file: {token_path}')
    with open(token_path, 'r') as f:
        return f.read()


def run(token_path):
    bot.run(read_token(token_path))
