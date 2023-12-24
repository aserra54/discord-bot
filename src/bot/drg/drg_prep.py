import logging

from disnake import ApplicationCommandInteraction
from disnake.ext.commands import Param
from bot import bot


LOGGER = logging.getLogger('redmac.bot.drg.drg_prep')

locations = ['Azure Weald', 'Crystalline Caverns', 'Dense Biozone', 'Fungus Bogs', 'Glacial Strata', 'Hollow Bough',
             'Magma Core', 'Radioactive Exclusion Zone', 'Salt Pits', 'Sandblasted Corridors']

mission_types = ['Deep Dive', 'Egg Hunt', 'Elimination', 'Escort Duty', 'Industrial Sabotage', 'Mining Expedition',
                 'On-site Refining', 'Point Extraction', 'Salvage Operation']

side_missions = ['Alien Fossils', 'Apoca Blooms', 'Boolo Caps', 'Dystrum', 'Ebonuts', 'Fester Fleas', 'Gunk Seeds', 
                 'Hollomite']

anomalies = ['-', 'Critical Weakness', 'Double XP', 'Gold Rush', 'Golden Bugs', 'Low Gravity', 'Mineral Mania', 
             'Rich Atmosphere', 'Volatile Guts']

mutators = ['-', 'Cave Leech Cluster', 'Elite Threat', 'Exploder Infestation!', 'Haunted Cave', 'Lethal Enemies',
            'Lithophage Outbreak', 'Low Oxygen', 'Mactera Plague', 'Parasites', 'Regenerative Bugs', 'Rival Presence',
            'Shield Disruption', 'Swarmageddon']


@bot.slash_command(name='drg-prep')
async def drg_prep(
    self,
    interaction: ApplicationCommandInteraction, 
    length: int = Param(choices=[1, 2, 3]),
    complexity: int = Param(choices=[1, 2, 3]),
    location: str = Param(choices=locations),
    mission_type: str = Param(choices=mission_types),
    side_mission: str = Param(choices=side_missions),
    anomaly: str = Param(choices=anomalies),
    mutator1: str = Param(choices=mutators),
    mutator2: str = Param(choices=mutators),
    game_type: str = Param(choices=['Solo', 'Multiplayer']),
):
    await DrgPrepCommand().handle(interaction, length, complexity, location, mission_type, side_mission, anomaly,
                                  mutator1, mutator2, game_type)


class DrgPrepCommand:
    '''Handles the 'drg-prep' slash command.'''

    async def handle(self, interaction: ApplicationCommandInteraction, length: int, complexity: int, location: str, mission_type: str, side_mission: str, anomaly: str, mutator1: str, mutator2: str, game_type: str):
        '''Given the parameters of a mission in Deep Rock Galactic (DRG), returns the computed hazard bonuses for the
        different difficult levels as well as suggested perks to use on those missions.'''

        base_bonus = 0
        base_bonus += (length - 1) * 10
        base_bonus += (complexity - 1) * 10
        base_bonus += self._get_hazard_bonus(mutator1)
        base_bonus += self._get_hazard_bonus(mutator2)

        passives, actives = self._get_suggested_perks(location, mission_type, side_mission, anomaly, mutator1, mutator2, game_type)

        messages = [
            '**__Mission Parameters__**',
            f'**Mission Length**: {length}',
            f'**Cave Complexity**: {complexity}',
            f'**Biome**: {location}',
            f'**Mission Type**: {mission_type}',
            f'**Side Mission**: {side_mission}',
            f'**Anomaly**: {anomaly}',
            f'**Mutators**: {mutator1}/{mutator2}',
            '',
            '**__Hazard Bonuses__**',
            f'**Hazard 1**: {base_bonus + 25}',
            f'**Hazard 2**: {base_bonus + 50}',
            f'**Hazard 3**: {base_bonus + 75}',
            f'**Hazard 4**: {base_bonus + 100}',
            f'**Hazard 5**: {base_bonus + 133}',
            '',
            '**__Suggested Passive Perks__**',
            '\n'.join(passives) if len(passives) > 0 else '-',
            '',
            '**__Suggested Active Perks__**',
            '\n'.join(actives) if len(actives) > 0 else '-',
        ]
        await interaction.response.send_message('\n'.join(messages))

    def _get_hazard_bonus(self, mutator):
        bonuses = {
            '-': 0,
            'Cave Leech Cluster': 15,
            'Elite Threat': 30,
            'Exploder Infestation!': 20,
            'Haunted Cave': 30,
            'Lethal Enemies': 25,
            'Lithophage Outbreak': 50,
            'Low Oxygen': 20,
            'Mactera Plague': 20,
            'Parasites': 15,
            'Regenerative Bugs': 15,
            'Rival Presence': 30,
            'Shield Disruption': 30,
            'Swarmageddon': 20,
        }
        if mutator not in bonuses:
            LOGGER.warning(f'Unknown mutator: {mutator}')
            return 0
        return bonuses[mutator]
    
    def _get_suggested_perks(self, location, mission_type, side_mission, anomaly, mutator1, mutator2, game_type):

        passives = set()
        actives = set()

        def add(type_, name, p, a):
            for perk, desc in p:
                passives.add(f'**{perk}**: {desc} (*{type_}: {name}*)')
            for perk, desc in a:
                actives.add(f'**{perk}**: {desc} (*{type_}: {name}*)')

        p, a = self._get_location_perks(location)
        add('Biome', location, p, a)

        p, a = self._get_mission_type_perks(mission_type)
        add('Mission', mission_type, p, a)

        p, a = self._get_side_mission_perks(side_mission)
        add('Side Mission', side_mission, p, a)

        p, a = self._get_anomaly_perks(anomaly)
        add('Anomaly', anomaly, p, a)

        p, a = self._get_mutator_perks(mutator1)
        add('Mutator', mutator1, p, a)
        p, a = self._get_mutator_perks(mutator2)
        add('Mutator', mutator2, p, a)

        p, a = self._get_game_type_perks(game_type)
        add('Game Type', game_type, p, a)

        return list(sorted(passives)), list(sorted(actives))
    
    def _get_location_perks(self, location):
        passives, actives = [], []
        if location == 'Crystalline Caverns':
            passives.append(('Elemental Insulation', 'Resistance against electricity damage'))
            passives.append(('Unstoppable', 'Useful for powering through spiderwebs and electrocrystals'))
            actives.append(('Dash', 'Useful for powering through spiderwebs and electrocrystals'))
        elif location == 'Dense Biozone':
            passives.append(('Unstoppable', 'Useful for powering through spiderwebs'))
            actives.append(('Dash', 'Useful for powering through spiderwebs'))
        elif location == 'Fungus Bogs':
            passives.append(('Unstoppable', 'Useful for powering through goo patches'))
            actives.append(('Dash', 'Useful for powering through goo patches'))
        elif location == 'Glacial Strata':
            passives.append(('Elemental Insulation', 'Resistance against frost and ambient cold damage'))
            passives.append(('Unstoppable', 'Useful for walking through heavy snow and blizzards'))
            actives.append(('Dash', 'Useful for walking through heavy snow and blizzards'))
        elif location == 'Hollow Bough':
            passives.append(('Unstoppable', 'Useful for powering through spiderwebs and the goo from goo sacks'))
            actives.append(('Dash', 'Useful for powering through spiderwebs and the goo from goo sacks'))
        elif location == 'Magma Core':
            passives.append(('Elemental Insulation', 'Resistance against fire and ambient heat damage'))
            passives.append(('Unstoppable', 'Useful for walking through earthquakes'))
            actives.append(('Dash', 'Useful for walking through earthquakes'))
        elif location == 'Radioactive Exclusion Zone':
            passives.append(('Elemental Insulation', 'Resistance against radiation damage'))
            passives.append(('Unstoppable', 'Useful for powering through spiderwebs'))
            actives.append(('Dash', 'Useful for powering through spiderwebs'))
        elif location == 'Sandblasted Corridors':
            passives.append(('Unstoppable', 'Useful for walking through sandstorms'))
            actives.append(('Dash', 'Useful for walking through sandstorms'))
        return passives, actives
    
    def _get_mission_type_perks(self, mission_type):
        passives, actives = [], []
        if mission_type == 'Deep Dive':
            passives.append(('Thorns', 'If the Swarmageddon mutator shows up, this will help immensely in dealing with them'))
            passives.append(('Vampire', 'Gives a way to restore health, which is scarce in deep dives (especially when combined with Berzerker)'))
            actives.append(('Berzerker', 'When combined with Vampire, gives an excellent way to restore health'))
            actives.append(('Heightened Senses', 'With how easy it is to die, this can save you from cave leeches and grabbers'))
            actives.append(('Iron Will', 'Can help in taking out the enemies that took you down'))
        elif mission_type == 'Egg Hunt':
            passives.append(('Strong Arm', 'Allows for throwing alien eggs further'))
            passives.append(('Unstoppable', 'Allows you to walk faster while carrying alien eggs'))
        elif mission_type == 'Elimination':
            passives.append(('Resupplier', 'Useful for getting a resupply faster during dreadnought fights'))
            actives.append(('Dash', 'Can help get out of tight situations during dreadnought fights'))
        elif mission_type == 'Escort Duty':
            passives.append(('Veteran Depositor', 'Planting Molly near Doretta will give you damage resistance during swarms'))
        elif mission_type == 'Industrial Sabotage':
            passives.append(('Resupplier', 'Useful for getting a resupply faster during the hectic end fight'))
            passives.append(('Strong Arm', 'Allows for throwing transmitter nodes further'))
            passives.append(('Unstoppable', 'Allows you to walk faster while carrying transmitter nodes'))
            actives.append(('Dash', 'Can help get out of tight situations during the end fight'))
        elif mission_type == 'Mining Expedition':
            passives.append(('Deep Pockets', 'These missions usually involve carrying a lot of materials, so the extra bag space is a bonus'))
            passives.append(('Second Wind', 'Most mining expeditions have long-winded tunnels where you will be sprinting for long periods of time; this will make you sprint faster'))
            passives.append(('Veteran Depositor', 'These missions usually involve carrying a lot of materials, so depositing faster is a bonus'))
        elif mission_type == 'On-site Refining':
            passives.append(('Veteran Depositor', 'The central refinery gives the damage resistance bonus, which is useful since most swarms will be dealt with there'))
        elif mission_type == 'Point Extraction':
            passives.append(('Strong Arm', 'Allows for throwing aquarqs further'))
            passives.append(('Unstoppable', 'Allows you to walk faster while carrying aquarqs'))
        return passives, actives

    def _get_side_mission_perks(self, side_mission):
        passives, actives = [], []
        if side_mission == 'Gunk Seeds':
            passives.append(('Strong Arm', 'Allows for throwing gunk seeds further'))
            passives.append(('Unstoppable', 'Allows you to walk faster while carrying gunk seeds'))
        return passives, actives

    def _get_anomaly_perks(self, anomaly):
        passives, actives = [], []
        if anomaly == 'Gold Rush':
            passives.append(('Deep Pockets', 'Since there will be a lot of gold, the extra bag space is a plus'))
            passives.append(('Veteran Depositor', 'Since there will be a lot of gold, the extra depositing speed is a plus'))
        elif anomaly == 'Golden Bugs':
            passives.append(('Deep Pockets', 'Since there will be a lot of gold, the extra bag space is a plus'))
            passives.append(('Veteran Depositor', 'Since there will be a lot of gold, the extra depositing speed is a plus'))
        elif anomaly == 'Mineral Mania':
            passives.append(('Deep Pockets', 'Since there will be many minerals, the extra bag space is a plus'))
            passives.append(('Veteran Depositor', 'Since there will be many minerals, the extra depositing speed is a plus'))
        elif anomaly == 'Rich Atmosphere':
            actives.append(('See You In Hell', 'Since enemies move much faster, the chance of being meleed is higher, giving this more use'))
        return passives, actives
    
    def _get_mutator_perks(self, mutator):
        passives, actives = [], []
        if mutator == 'Cave Leech Cluster':
            actives.append(('Dash', 'Can be a decent fallback for outrunning cave leeches'))
            actives.append(('Heightened Senses', 'Instantly kills a cave leech that grabs you'))
        elif mutator == 'Exploder Infestation!':
            actives.append(('Dash', 'Can be a decent fallback for outrunning exploders'))
        elif mutator == 'Haunted Cave':
            actives.append(('Dash', 'Can be a decent fallback for outrunning the haunted ghost'))
        elif mutator == 'Lethal Enemies':
            passives.append(('Thorns', 'Since enemy melee damage hurts more, then ensuring they take damage if they touch you will help kill bugs faster'))
        elif mutator == 'Low Oxygen':
            passives.append(('Veteran Depositor', 'Since you need to stay near deposit points (e.g. the mule) anyway, the bonus will always kick in'))
        elif mutator == 'Mactera Plague':
            actives.append(('Heightened Senses', 'Grabbers will appear more often, and this allows you to instantly kill any that grab you'))
        elif mutator == 'Regenerative Bugs':
            actives.append(('Beast Master', "The mutator applies to your minion as well, allowing them to heal throughout the mission"))
        elif mutator == 'Rival Presence':
            actives.append(('Dash', 'Can be a decent fallback for outrunning Nemesis (if it appears)'))
            actives.append(('Heightened Senses', 'If a Nemesis appears, this allows you to escape its grab attack instantaneously'))
        elif mutator == 'Shield Disruption':
            passives.append(('Resupplier', 'Gives additional health when resupplying, which is important with no shields'))
            passives.append(('Sweet Tooth', 'Makes Red Sugar give additional health, which is important with no shields'))
            passives.append(('Vampire', 'Gives another way to restore health, which is important with no shields (especially when combined with Berzerker)'))
            actives.append(('Berzerker', 'When combined with Vampire, gives an excellent way to restore health'))
        elif mutator == 'Swarmageddon':
            passives.append(('Thorns', 'Swarmers die immediately if they touch you with this perk'))
            actives.append(('See You In Hell', 'Since swarmers move fast, the chance of being meleed is higher, giving this more use'))
        return passives, actives

    def _get_game_type_perks(self, game_type):
        passives, actives = [], []
        if game_type == 'Multiplayer':
            passives.append(('Friendly', 'Lowers impact of friendly fire'))
            passives.append(('Sweet Tooth', 'Gives you more health from Red Sugar, allowing it to be better distributed to teammates'))
            actives.append(('Field Medic', 'Good for insta-reviving teammates in tight situations'))
            actives.append(('Iron Will', 'Allows for better repositioning after going down to help teammates revive you easier'))
            actives.append(('Shield Link', 'Assuming no Shield Disruption mutator, gives an excellent way to overcharge teammates\' shields'))
        return passives, actives
