from dev.safe_print import safe_print

import asyncio
import re

class HighlowCommand:
    def __init__(self, bot):
        self.bot = bot


    async def run(self):
        await self.bot.send_cmd('highlow')

        msg = await self.bot.wait_for_event('message')
        if msg is None: 
            return
        
        desc = msg.embeds[0].description.lower()

        numbers = re.findall(r'\d+', desc)
        if len(numbers) < 3:
            return
        
        number = int(numbers[2])

        if number < 50:
            btn_num = 2
        else:
            btn_num = 0

        await self.bot.click(msg, 0, btn_num)

        msg_edit = await self.bot.wait_for_event('message_edit')
        if msg_edit is None:
            return

        items, coins = self.bot.get_rewards_from_text(msg_edit.embeds[0].description)
        print(items, coins)