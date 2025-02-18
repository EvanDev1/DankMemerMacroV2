from dev.safe_print import safe_print

import asyncio
import re

class ScrapeInventory:
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def extract_item(text):
        pattern = r"\*\*<:[^>]+> ([^*]+)\*\* \u2500 (\d+)"
        match = re.search(pattern, text)
        if match:
            item_name = match.group(1)
            amount = int(match.group(2))
            return item_name, amount
        return None, None

    async def run(self):
        await self.bot.send_cmd('inventory')

        msg = await self.bot.wait_for_event('message')
        if msg is None: 
            return
        
        pages = int(re.findall(r'\d+', msg.embeds[0].footer.text)[1])

        inventory = {}

        for x in range(pages):
            desc = msg.embeds[0].description.lower()
            lines = desc.split('\n')

            for i in range(0, len(lines), 3):
                safe_print(lines[i])
                item, amount = self.extract_item(lines[i])
                if item == 'new player pack':
                    # Use new player pack
                    await self.bot.safe_delay()
                    await self.bot.send_cmd('use', item="new player pack")
                    await self.bot.safe_delay()
                    return await self.run()
                inventory[item] = amount

            if x < pages - 1:
                await self.bot.click(msg, 1, 2)
                msg = await self.bot.wait_for_event('message_edit')

        return inventory