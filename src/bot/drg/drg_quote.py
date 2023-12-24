import random
from disnake import ApplicationCommandInteraction
from bot import bot


quotes = [
    ('Where is that damn tin can?!', 'Dwarf', 'when calling for the MULE'),
    ('I need the damn minecart on legs! Where is it?!', 'Dwarf', 'when calling for the MULE'),
    ("Help! I'm stuck in the ceiling!", 'Dwarf', 'when grabbed by a cave leech'),
    ('From A to D, skipping B and C!', 'Scout', 'when using the grappling hook'),
    ('Ready to blow!', 'Driller', 'when placing a satchel charge'),
]


@bot.slash_command(name='drg-quote')
async def drg_quote(self, interaction: ApplicationCommandInteraction):
    await DrgQuoteCommand().handle(interaction)


class DrgQuoteCommand:
    async def handle(self, interaction):
        quote, speaker, situation = random.choice(quotes)
        message = f'"{quote}" - {speaker}, {situation}'
        await interaction.response.send_message(message)
