from dev.safe_print import safe_print

# Just make a priority list of all the places to go
# and then the user can edit it based on what item they wanna get
# idk



import asyncio

class CrimeCommand:
    def __init__(self, bot):
        self.bot = bot


    async def run(self):
        await self.bot.send_cmd('crime')

        msg = await self.bot.wait_for_event('message')
        if msg is None: 
            return