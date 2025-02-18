import asyncio
import re

from dev.safe_print import safe_print

##### YOU NEED TO SPEND HOURS AND HOURS TO DO THE MOLE MAN AND PINK SLUDGE MONSTER
##### BOSS THINGIES IDFK

class DigCommand:

    moleman_loc = {
        "<a:MoleMan:1022972147175526441><:emptyspace:827651824739156030><:emptyspace:827651824739156030>": (
            0
        ),
        "<:emptyspace:827651824739156030><a:MoleMan:1022972147175526441><:emptyspace:827651824739156030>": (
            1
        ),
        "<:emptyspace:827651824739156030><:emptyspace:827651824739156030><a:MoleMan:1022972147175526441>": (
            2
        ),
    }

    worms_loc = {
        "<:emptyspace:827651824739156030><:Worm:864261394920898600><:Worm:864261394920898600>": (
            0
        ),
        "<:Worm:864261394920898600><:emptyspace:827651824739156030><:Worm:864261394920898600>": (
            1
        ),
        "<:Worm:864261394920898600><:Worm:864261394920898600><:emptyspace:827651824739156030>": (
            2
        ),
    }


    def __init__(self, bot):
        self.bot = bot


    async def run(self):
        await self.bot.send_cmd('dig')

        msg = await self.bot.wait_for_event('message')
        if msg is None: 
            return
        
        desc = msg.embeds[0].description.lower()
        
        broken = "you don't have a shovel" in desc
        just_broke = "shovel also broke" in desc

        if broken or just_broke:
            success = await self.bot.buy_item('shovel', 1)
            if success:
                print('bought shovel :)')
                if broken:
                    await self.run()
                    return
        safe_print(desc)

        if "look at each color next to the words closely" in desc:
            success = await self.mole_man_event(msg)
            print(success, "mole man success")
        elif "remember words order" in desc:
            success = await self.sludge_monster_event(msg)
            print(success, "sludge monster success")
        elif "dunk the ball!" in desc:
            success = await self.dunk_event(msg)
            print(success, "dunk event")

        items, coins = self.bot.get_rewards_from_text(desc)
        print(items, coins)

        await asyncio.sleep(35)
        if self.bot.captcha == True:
            print('Detected captcha and stopped running dig command!!')
            return
        await self.run()

    async def sludge_monster_event(self, msg):
        desc = msg.emebeds[0].description.lower()

        msg_edit = await self.bot.wait_for_event('message_edit')
        if msg_edit is None:
            return
        
        lines = desc.split("\n")
        lines.pop(0)
        words = [line.strip('`') for line in lines]

        await self.bot.safe_delay()

        for word in words:
            click_state = await self.bot.click(msg_edit, 0, word)
            if click_state is False:
                return
        
        reward_msg = await self.bot.wait_for_event('message_edit')
        if reward_msg is None:
            return

        items, coins = self.bot.get_rewards_from_text(reward_msg.embeds[0].description)
        print(items, coins)
        print('PINK SLUDGE FINISHED WHOOO')
        return True

    async def mole_man_event(self, msg):
        desc = msg.embeds[0].description.lower()

        # Initialize the dictionary
        colors = {}
        print(colors)

        # Iterate through each line
        for line in desc.strip().splitlines()[1:]:
            # Use regex to extract the color and keyword
            match = re.search(r'<:(\w+):\d+> `(\w+)`', line)
            if match:
                color, keyword = match.groups()
                colors[keyword] = color

        msg_edit = await self.bot.wait_for_event('message_edit', timeout=10)
        if msg_edit is None:
            return
        
        print(msg_edit.embeds[0].description)

        word = re.search(r'`(.*?)`', msg_edit.embeds[0].description).group(1)
        print(word)
        
        click_state = await self.bot.click(msg_edit, 0, word)
        if click_state is False:
            return
        
        reward_msg = await self.bot.wait_for_event('message_edit')
        if reward_msg is None:
            return
        
        items, coins = self.bot.get_rewards_from_text(reward_msg.embeds[0].description.lower())
        print(items, coins)
        print('MOLE MAN FINISHED WHOOO')
        return True
    
    async def dunk_event(self, msg):
        desc = msg.embeds[0].description.lower()
        print("------------------")
        print("DUNK EVENT")
        print("------------------")
        while True:
            msg_edit = self.bot.wait_for_event("message_edit")
            safe_print(msg_edit.embeds[0].description.lower)
            print('---------------------------')



# soccer thingy
# hit the ball!
# :goal::goal::goal:
# <:emptyspace:827651824739156030>:levitate:

# <:emptyspace:827651824739156030>:soccer: