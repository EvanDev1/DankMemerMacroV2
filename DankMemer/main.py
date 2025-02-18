##### ISSUES:
# sometimes interactions don't work and say Hold Tight! in the title sooo fix that :)
# get level up rewards and add to inventory


import asyncio
import random
import discord

from bot import Bot

# example data that would be sent from the app
data = {
    'tokens': [
        # list of tokens
    ],
    'channel_ids': [
        1261090793796534292,
        1268305154558398527,
        1268305176150937661
    ],
    'bot_data': {
        'postmemes': {
            'platform': 'tiktok',
            'meme_type': 'repost'
        }
    },
    'settings':{
        'scrape_inv_on_load': True
    }
}

class ClientsHandler:
    # Handle each bot
    def __init__(self):
        self.clients = []

    async def schedule_tasks(tasks, total_time):
        num_tasks = len(tasks)
        interval = total_time / num_tasks
        
        # Generate random start times for each task within their respective intervals
        start_times = [random.uniform(i * interval, (i + 1) * interval) for i in range(num_tasks)]
        start_times.sort()

        async def run_tasks():
            previous_start_time = 0
            for i, start_time in enumerate(start_times):
                delay = start_time - previous_start_time
                await asyncio.sleep(delay)  # Delay before starting each task
                print(f"Executing task {i+1} at {start_time:.2f} seconds (delay: {delay:.2f} seconds)")
                # Execute the function
                tasks[i]()
                previous_start_time = start_time

        await run_tasks()


    async def start_bot(self, token, channel_id):
        # Start an individual bots
        client = Bot(channel_id=channel_id, settings=data['settings'])
        self.clients.append(client)
        try:
            await client.start(token)

        except discord.errors.LoginFailure:
            client.token_failed = True
            print('-----------------------------------')
            print(f"LOGIN FAILED FOR TOKEN: {token}")
            print('-----------------------------------')

    async def start_bots(self):
        # Create a bot for every token
        tasks = []
        channel_index = 0

        random.shuffle(data['tokens'])

        for token in data['tokens']:
            channel_id = data['channel_ids'][channel_index]
            tasks.append(self.start_bot(token, channel_id))

            channel_index += 1
            if channel_index == len(data['channel_ids']):
                channel_index = 0

        await asyncio.gather(*tasks)

    async def start_autofarm(self):
        # Star the auto_farm function for each bot

        SAFE_START_TIME = 10  # 60 seconds
        num_selfbots = len(self.clients)
        print('selfbots_num', num_selfbots)

        interval = SAFE_START_TIME / num_selfbots
        start_times = [random.uniform(i * interval, (i + 1) * interval) for i in range(num_selfbots)]
        start_times.sort()

        previous_start_time = 0
        for i, start_time in enumerate(start_times):
            delay = start_time - previous_start_time
            await asyncio.sleep(delay)  # Delay before starting each selfbot
            print(f"Starting selfbot {i+1} at {start_time:.2f} seconds (delay: {delay:.2f} seconds)")

            # Replace the print and sleep with actual selfbot starting code
            # start_selfbot(i+1)
            previous_start_time = start_time


        # startup_delay = 15 # ADD THIS FEATURE FSSSS
        print(self.clients)
        for client in self.clients:
            await client.safe_delay(min_delay=3, max_delay=6)
            client.auto_farm()

async def main():
    handler = ClientsHandler()

    await handler.start_bots()
    print('Starting autofarm!!')

    await handler.start_autofarm()


if __name__ == "__main__":
    asyncio.run(main())
