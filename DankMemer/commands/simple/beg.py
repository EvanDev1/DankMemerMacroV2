from dev.safe_print import safe_print
from dev.print_time import print_time
import asyncio


class BegCommand():
    profit = 0
    def __init__(self, bot):
        self.bot = bot

    async def run(self):
        print_time('Sending command...')
        await self.bot.send_cmd('beg')
        print_time('Command sent...')

        msg = await self.bot.wait_for_event('message')
        print_time('Received message event...')
        desc = msg.embeds[0].description

        loot = {}

        coins = self.bot.get_coins_from_text(desc)
        if coins:
            self.profit += coins
            loot['coins'] = coins

        amount, item_name = self.bot.get_item_from_text(desc)
        if amount:
            loot[item_name] = amount

        print(loot)
        print('Profit: ', self.profit)
        
        await asyncio.sleep(42)
        await self.run()
        
# 14:40:19.042211 start
# 