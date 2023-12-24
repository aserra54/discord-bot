import json
import random
from disnake import ApplicationCommandInteraction
from bot import bot


DATA_JSON = 'data/drg-quotes.json'


@bot.slash_command(name='drg-quote', description='Returns a random quote from Deep Rock Galactic.')
async def drg_quote(self, interaction: ApplicationCommandInteraction):
    await DrgQuoteCommand().handle(interaction)


class DrgQuoteCommand:
    '''Command for returning a random quote from Deep Rock Galactic.'''

    async def handle(self, interaction):
        with open(DATA_JSON, mode='r', encoding='utf-8') as f:
            data = json.loads(f.read())
        quotes = data['quotes']

        selected = random.choice(quotes)
        quote = selected['quote']
        source = selected['source']
        scenario = selected['scenario']

        message = f'"{quote}" - {source}, {scenario}'
        await interaction.response.send_message(message)
