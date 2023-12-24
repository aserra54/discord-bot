import random
from disnake import ApplicationCommandInteraction
from bot import bot


quotes = [
    ('Where is that damn tin can?!', 'Dwarf', 'when calling for the MULE'),
    ('I need the damn minecart on legs! Where is it?!', 'Dwarf', 'when calling for the MULE'),
    ("Help! I'm stuck in the ceiling!", 'Dwarf', 'when grabbed by a cave leech'),
    ('From A to D, skipping B and C!', 'Scout', 'when using the grappling hook'),
    ('Ready to blow!', 'Driller', 'when placing a satchel charge'),
    ('I call it my "grenade-grenade"!', 'Gunner', 'when throwing a cluster grenade'),
    ('Multi-boom!', 'Gunner', 'when throwing a cluster grenade'),
    ("Turrets and explosions! You've come to the right place, mate.", 'Engineer', 'when selected'),
    ('Two-thousand rounds of depleted uranium, aw yeah!', 'Gunner', 'when selected'),
    ('Allow me to "illuminate" the situation! Hahahaha!', 'Scout', 'when selected'),
    ("If it ain't drillable, it's probably flammable.", 'Driller', 'when selected'),
]


@bot.slash_command(name='drg-quote', description='Returns a random quote from Deep Rock Galactic.')
async def drg_quote(self, interaction: ApplicationCommandInteraction):
    await DrgQuoteCommand().handle(interaction)


class DrgQuoteCommand:
    async def handle(self, interaction):
        quote, speaker, situation = random.choice(quotes)
        message = f'"{quote}" - {speaker}, {situation}'
        await interaction.response.send_message(message)
