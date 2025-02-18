import asyncio

class BuyItem():
    shop = [
        { # Page 1
            'shovel': 50000,
            'hunting rifle': 50000,
            'mouse': 100000,
            'keyboard': 100000,
            'adventure ticket': 250000,
            'bank note': 250000,
        },
        { # Page 2
            'watering can': 75000,
            'hoe': 100000,
            'bean seeds': 35000,
            'potato seeds': 50000,
            'corn seeds': 85000,
            'carrot seeds': 125000,
        },
        { # Page 3
            'pepe trophy': 35000000,
            'pepe crown': 120000000,
            'life saver': 250000,
            'apple': 45000,
            'engagement ring': 5000000,
            'shredded cheese': 250000,
        },
        { # Page 4
            'cell phone': 10000,
            'padlock': 50000,
            'landmine': 150000,
            'box of sand': 25000,
            'robbers wishlist': 500000,
            'alcohol': 85000,
        },
    ]
    def __init__(self, bot):
        self.bot = bot

    async def run(self, item_name, amount):
        await self.bot.send_cmd('shop view')

        msg = await self.bot.wait_for_event('message')
        if msg is None:
            return

        await self.bot.select_option(msg, 0, 0)

        page_num = None
        btn_num = None
        btn_comp = None

        for i, page in enumerate(self.shop):
            if item_name in page:
                page_num = i + 1

                btn_num = list(page.keys()).index(item_name)
                btn_comp = 1 if btn_num < 3 else 2

                break

        if page_num is None:
            print(f"{item_name} is not an item listed in the shop.")
            return False

        clicks = page_num
        if page_num < 4:
            clicks = page_num - 1
            arrow_num = 1
        else:
            clicks = 1
            arrow_num = 0

        print(clicks, page_num)

        for x in range(clicks):
            if await self.bot.click(msg, 3, arrow_num) is None:
                return
            msg = await self.bot.wait_for_event('message_edit')
            if msg is None:
                return

        while True:
            if await self.bot.click(msg, btn_comp, int(btn_num)) is None:
                return
            
            modal = await self.bot.wait_for_event('modal', timeout=10)
            if modal is None:
                print('Error with modal!!')
                continue

            await self.bot.submit_modal(modal, str(amount))
            break

        buy_msg = await self.bot.wait_for_event('message_reply', reply_msg=msg)
        if buy_msg:
            return True