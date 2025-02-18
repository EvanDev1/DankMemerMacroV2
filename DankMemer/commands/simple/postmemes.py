import re
import asyncio

from dev.safe_print import safe_print


class PostmemesCommand:
    def __init__(self, bot):
        self.bot = bot

    async def run(self):
        await self.bot.send_cmd('postmemes')

        msg = await self.bot.wait_for_event('message')

        # check cooldown
        if self.bot.check_cooldown(msg):
            print('message on cooldown still idiot!!')
            return

        # set options
        platform = "facebook"
        meme = "repost"

        await self.bot.select_option(msg, 0, platform)
        await self.bot.select_option(msg, 1, meme)

        if await self.bot.click(msg, 2, 0) is None:
            print('Failed button interaction!!')
            # return
        
        msg_edit = await self.bot.wait_for_event('message_edit')
        desc = msg_edit.embeds[0].description.lower()

        if "you posted a dead meme" in desc:
            print('Dead meme! Cooldown needs to be set to 3 mins now :c')
            return

        if not "you received" in desc: # no earnings
            print('no earnings :c')
            return
        
        loot_rows = desc.split("**you received:**")[1].strip().split('\n')

        loot = {}

        for row in loot_rows:
            coins = self.bot.get_coins_from_text(row)
            if coins:
                loot['coins'] = coins
                continue
            
            amount, item_name = self.bot.get_item_from_text(row)

            if amount is not None:
                loot[item_name] = amount

        print(loot)

        await asyncio.sleep(32)
            