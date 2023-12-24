import disnake
import logging


LOGGER = logging.getLogger('redmac.cmd')


class CommandHandler:
    '''Central class for handling slash commands.'''

    async def handle_drg(self, interaction: disnake.ApplicationCommandInteraction, length: int, complexity: int, location: str, mission_type: str, anomaly: str, mutator1: str, mutator2: str):
        '''Given the parameters of a mission in Deep Rock Galactic (DRG), returns the computed hazard bonuses for the
        different difficult levels as well as suggested perks to use on those missions.'''

        base_bonus = 0
        base_bonus += (length - 1) * 10
        base_bonus += (complexity - 1) * 10
        base_bonus += self._get_hazard_bonus(mutator1)
        base_bonus += self._get_hazard_bonus(mutator2)

        passives = self._get_suggested_passive_perks(length, complexity, location, mission_type, anomaly, mutator1, mutator2)
        actives = self._get_suggested_active_perks(length, complexity, location, mission_type, anomaly, mutator1, mutator2)

        messages = [
            '**__Mission Parameters__**',
            f'**Mission Length**: {length}',
            f'**Cave Complexity**: {complexity}',
            f'**Biome**: {location}',
            f'**Mission Type**: {mission_type}',
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
            '**__Suggested Perks__**',
            f"**Passive**: {', '.join(passives) if len(passives) > 0 else '-'}",
            f"**Active**: {', '.join(actives) if len(actives) > 0 else '-'}",
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

    def _get_suggested_passive_perks(self, length, complexity, location, mission_type, anomaly, mutator1, mutator2):

        perks = set()

        # location
        if location in ('Fungus Bogs', 'Magma Core'):
            perks.add('Unstoppable')
        if location in ('Magma Core'):
            perks.add('Elemental Insulation')

        # mission types
        if mission_type in ('Egg Hunt', 'Mining Expedition'):
            perks.add('Deep Pockets')

        # anomalies
        if anomaly in ('Gold Rush', 'Golden Bugs', 'Mineral Mania'):
            perks.add('Deep Pockets')
        
        # mutators
        if 'Lethal Enemies' in (mutator1, mutator2):
            perks.add('Thorns')
        if 'Low Oxygen' in (mutator1, mutator2):
            perks.add('Veteran Depositor')
        if 'Shield Disruption' in (mutator1, mutator2):
            perks.add('Sweet Tooth')
            perks.add('Vampire')
        if 'Swarmageddon' in (mutator1, mutator2):
            perks.add('Thorns')
        
        return list(sorted(perks))
    
    def _get_suggested_active_perks(self, length, complexity, location, mission_type, anomaly, mutator1, mutator2):
        perks = set()
        if 'Cave Leech Cluster' in (mutator1, mutator2):
            perks.add('Heightened Senses')
        if 'Regenerative Bugs' in (mutator1, mutator2):
            perks.add('Beast Master')
        if 'Rival Presence' in (mutator1, mutator2):
            perks.add('Heightened Senses')
        return list(sorted(perks))
