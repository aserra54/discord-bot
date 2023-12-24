import app
import disnake
import os
from disnake.ext import commands


# setup the bot globally
INTENTS = disnake.Intents.default()
INTENTS.message_content = True
bot = commands.Bot(intents=INTENTS, command_prefix='!')
app = app.App()


@bot.event
async def on_ready():
    app.initialize(bot, 'rules.json')


@bot.event
async def on_message(message):
    await app.message_handler.handle(bot, message)


@bot.slash_command()
async def drg(
    self,
    interaction: disnake.ApplicationCommandInteraction, 
    length: int = commands.Param(choices=[1, 2, 3]),
    complexity: int = commands.Param(choices=[1, 2, 3]),
    location: str = commands.Param(choices=['Azure Weald', 'Crystalline Caverns', 'Dense Biozone', 'Fungus Bogs', 'Glacial Strata', 'Hollow Bough', 'Magma Core', 'Radioactive Exclusion Zone', 'Salt Pits', 'Sandblasted Corridors']),
    mission_type: str = commands.Param(choices=['Deep Dive', 'Egg Hunt', 'Elimination', 'Escort Duty', 'Industrial Sabotage', 'Mining Expedition', 'On-site Refining', 'Point Extraction', 'Salvage Operation']),
    side_mission: str = commands.Param(choices=['Alien Fossils', 'Apoca Blooms', 'Boolo Caps', 'Dystrum', 'Ebonuts', 'Fester Fleas', 'Gunk Seeds', 'Hollomite']),
    anomaly: str = commands.Param(choices=['-', 'Critical Weakness', 'Double XP', 'Gold Rush', 'Golden Bugs', 'Low Gravity', 'Mineral Mania', 'Rich Atmosphere', 'Volatile Guts']),
    mutator1: str = commands.Param(choices=['-', 'Cave Leech Cluster', 'Elite Threat', 'Exploder Infestation!', 'Haunted Cave', 'Lethal Enemies', 'Lithophage Outbreak', 'Low Oxygen', 'Mactera Plague', 'Parasites', 'Regenerative Bugs', 'Rival Presence', 'Shield Disruption', 'Swarmageddon']),
    mutator2: str = commands.Param(choices=['-', 'Cave Leech Cluster', 'Elite Threat', 'Exploder Infestation!', 'Haunted Cave', 'Lethal Enemies', 'Lithophage Outbreak', 'Low Oxygen', 'Mactera Plague', 'Parasites', 'Regenerative Bugs', 'Rival Presence', 'Shield Disruption', 'Swarmageddon']),
    game_type: str = commands.Param(choices=['Solo', 'Multiplayer']),
):
    await app.command_handler.handle_drg(interaction, length, complexity, location, mission_type, side_mission, anomaly, mutator1, mutator2, game_type)


def read_token(token_path):
    if not os.path.isfile(token_path):
        raise ValueError(f'No such file: {token_path}')
    with open(token_path, 'r') as f:
        return f.read()


if __name__ == '__main__':
    bot.run(read_token('.token'))
