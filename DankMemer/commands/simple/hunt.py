from dev.safe_print import safe_print

import asyncio

class HuntCommand:
    def __init__(self, bot):
        self.bot = bot


    async def run(self):
        await self.bot.send_cmd('hunt')

        msg = await self.bot.wait_for_event('message')
        if msg is None: 
            return
        
        desc = msg.embeds[0].description.lower()
        
        broken = "you don't have a hunting rifle" in desc
        just_broke = "hunting rifle broke" in desc

        if broken or just_broke:
            success = await self.bot.buy_item('hunting rifle', 1)
            if success:
                print('bought hunting rifle :)')
                if broken:
                    await self.run()
                    return


        if 'dodge the fireball' in desc:
            print('DRAGON EVENT !!!!!!')
            success = await self.dragon_event(msg)
            if success:
                print('won one dragon and 0 coins')
                return {'dragon': 1}, 0 # 1 dragon and 0 coins
            else:
                print('You died to dragon maybe???')

        items, coins = self.bot.get_rewards_from_text(desc)
        print(items, coins)

        await asyncio.sleep(35)
        if self.bot.captcha == True:
            print('Detected captcha and stopped running hunt command!!')
            return
        await self.run()
    


    async def dragon_event(self, msg):
        # default is left side
        middle = "<:emptyspace:827651824739156030>" # in middle
        right = "<:emptyspace:827651824739156030><:emptyspace:827651824739156030>" # right side

        desc = msg.embeds[0].description

        correct_button = 1
        if desc.split('\n')[2].startswith(middle):
            correct_button = 2
        if desc.split('\n')[2].startswith(right):
            correct_button = 1
        click_state = await self.bot.click(msg, 0, correct_button)

        if click_state is False:
            print('Hunt || Failed to click button.')
            while True:
                msg_edit = await self.bot.wait_for_event('message_edit')
                try:
                    if all([btn.disabled for btn in msg_edit[1].components[0].children]) is True:
                        break
                except:
                    break
                print(f'Hunt || Finished waiting for interaction to be over.')
                return True
        
        return True