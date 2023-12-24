from disnake import ApplicationCommandInteraction
from disnake.exts.commands import Param

from ..init import app, bot


zones = ['Azure Weald', 'Crystalline Caverns', 'Dense Biozone', 'Fungus Bogs', 'Glacial Strata', 'Hollow Bough', 'Magma Core', 'Radioactive Exclusion Zone', 'Salt Pits', 'Sandblasted Corridors']
mutators = ['-', 'Cave Leech Cluster', 'Elite Threat', 'Exploder Infestation!', 'Haunted Cave', 'Lethal Enemies', 'Lithophage Outbreak', 'Low Oxygen', 'Mactera Plague', 'Parasites', 'Regenerative Bugs', 'Rival Presence', 'Shield Disruption', 'Swarmageddon']


@bot.slash_command()
async def drg(
    self,
    interaction: ApplicationCommandInteraction, 
    length: int = Param(choices=[1, 2, 3]),
    complexity: int = Param(choices=[1, 2, 3]),
    location: str = Param(choices=zones),
    mission_type: str = Param(choices=['Deep Dive', 'Egg Hunt', 'Elimination', 'Escort Duty', 'Industrial Sabotage', 'Mining Expedition', 'On-site Refining', 'Point Extraction', 'Salvage Operation']),
    side_mission: str = Param(choices=['Alien Fossils', 'Apoca Blooms', 'Boolo Caps', 'Dystrum', 'Ebonuts', 'Fester Fleas', 'Gunk Seeds', 'Hollomite']),
    anomaly: str = Param(choices=['-', 'Critical Weakness', 'Double XP', 'Gold Rush', 'Golden Bugs', 'Low Gravity', 'Mineral Mania', 'Rich Atmosphere', 'Volatile Guts']),
    mutator1: str = Param(choices=mutators),
    mutator2: str = Param(choices=mutators),
    game_type: str = Param(choices=['Solo', 'Multiplayer']),
):
    await app.command_handler.handle_drg(interaction, length, complexity, location, mission_type, side_mission, anomaly, mutator1, mutator2, game_type)
