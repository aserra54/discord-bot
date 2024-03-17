import disnake
import random
import util.jsoncacher as jsoncacher
from disnake.ext import tasks, commands


DATA_JSON = 'data/drg-activities.json'


class DrgActivityTask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def start(self):
        self.change_activity.start()

    def cog_unload(self):
        self.change_activity.cancel()

    @tasks.loop(minutes=60.0)
    async def change_activity(self):
        data = jsoncacher.get(DATA_JSON)
        activities = data['activities']

        selected = random.choice(activities)
        type_ = selected['type']
        if type_ == 'playing':
            activity = disnake.Game(name=selected['name'])
            status = disnake.Status.online
        elif type_ == 'watching':
            activity = disnake.Activity(name='a movie',
                                        type=disnake.ActivityType.watching,
                                        state=selected['name'])
            status = disnake.Status.do_not_disturb
        elif type_ == 'listening':
            activity = disnake.Activity(name='music',
                                        type=disnake.ActivityType.listening,
                                        state=selected['name'])
            status = disnake.Status.online
        elif type_ == 'custom':
            activity = disnake.CustomActivity(
                name='Custom Status', state=selected['name'])
            status = selected['status']
        else:
            return
        await self.bot.change_presence(status=status, activity=activity)
