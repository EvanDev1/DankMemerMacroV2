import discord
import asyncio
import logging
import importlib
import os
import random
import re

from typing import Union

from utils.import_commands import import_commands
from utils.load_actions import load_actions

from dev.safe_print import safe_print

# Set up logging for debugging purposes
logging.basicConfig(level=logging.INFO)

class Bot(discord.Client):
    dank_id = 270904126974590976

    def __init__(self, channel_id, settings):
        super().__init__()
        self.channel_id = channel_id
        self.params = settings

        self.cmds = import_commands(self)
        load_actions(self)
        # actions

        self.ready = False
        self.token_failed = False
        self.captcha = False

        self.inventory = {}

    async def wait_for_event(self, event,  timeout=5, reply_msg=None):
        # Wait for a message or message_edit event and
        # return the message data that is sent
        def embed_check(msg, msg_edit=None):
            # Make sure it's the correct message
            return (
                msg.author.id == 270904126974590976 and
                msg.embeds and
                hasattr(msg, 'interaction') and
                hasattr(msg.interaction, 'user') and
                msg.interaction.user.id == self.user.id
            )
        def message_reply_check(msg):
            return (
                msg.reference and 
                msg.reference.message_id == reply_msg.id and
                msg.author.id == 270904126974590976 and
                msg.embeds
            )

        
        try:
            if event == 'message':
                msg = await self.wait_for(event, check=embed_check, timeout=timeout)
                return msg
            if event == 'message_edit':
                msg, msg_edit = await self.wait_for(event, check=embed_check, timeout=timeout)
                await asyncio.sleep(2) # sometimes it won't load the edit immediately so buttons can't be clicked
                return msg_edit
            if event == 'modal':
                # check to see if you can receive modals meant for other people?
                # i don't think so but maybe?
                modal = await self.wait_for(event, timeout=timeout)
                return modal
            if event == 'message_reply':
                if not reply_msg:
                    raise ValueError("msg_reply argument must be provided for 'message_reply' event")
                msg = await self.wait_for('message', check=message_reply_check, timeout=timeout)
                return msg

        except TimeoutError as e:
            print(f"Timeout error while waiting for {event} event!")
    
    async def on_ready(self):
        # Start the autofarm once the bot is ready
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('-------------------------')

        try:
            channel = await self.fetch_channel(self.channel_id)
            self.commands = await channel.application_commands()
        except Exception as e:
            print(f"Error in on_ready: {e}")

        if self.params['scrape_inv_on_load'] == True:
            self.inventory = await self.scrape_inventory()
            print(self.inventory)

        self.ready = True

    async def send_cmd(self, cmd, **kwargs):
        # Send a slash command including sub commands and options
        # /beg
        # /fish bucket
        # /withdraw amount=5000

        # Get command names
        cmds = cmd.split()
        cmd_name = cmds[0]
        sub_cmd_name = None
        if len(cmds) > 1:
            sub_cmd_name = cmds[1]

        while True:
            try:
                # Main command data
                command = next(
                    cmd for cmd in self.commands 
                    if cmd.name == cmd_name and cmd.application.id == 270904126974590976
                )
                if sub_cmd_name is None:
                    # Send main command
                    message = await command(**kwargs)
                else:
                    # Sub command data
                    sub_command = next(
                        subcmd for subcmd in command.children 
                        if subcmd.name.lower() == sub_cmd_name.lower()
                    )
                    # Send sub command
                    message = await sub_command()  # Call the subcommand directly
            except discord.Forbidden:
                print("Missing Permissions: Bot doesn't have the required permissions to send messages.\nAutofarming has been disabled.")
                return False
            except discord.HTTPException:
                print("Normal Send || HttpException")
                await asyncio.sleep(0.25)
                continue
            except discord.InvalidData:
                print("InvalidData: Did not receive a response from Discord")
            else:
                break
 
        return message

    async def on_message(self, msg):
        if msg.author.id != 270904126974590976 or len(msg.embeds) < 1:
            return
        
        title = None
        desc = None
 

        if msg.embeds[0].title is not None:
            title = msg.embeds[0].title.lower()
        if msg.embeds[0].description is not None:
            desc = msg.embeds[0].description.lower()
        

        # Ephemeral message
        if msg.flags.ephemeral:
            print('Ephemeral message!!')
            
            if title == "you have an unread alert!":
                # probably need to push this to a queue in the future
                await self.safe_delay()
                await self.send_cmd('alert') # this needs to be added to the cmd queue
        
            desc = msg.embeds[0].description.lower()
            if desc is not None and "to run commands you must pass captcha" in desc:
                print("------------------------------------------------------")
                print("CAPTCHA DETECTED ON ACCOUNT")
                print("------------------------------------------------------")
                self.captcha = True

        # Private DM
        if isinstance(msg.channel, discord.DMChannel):
            print('Received a private DM!')
            
            if desc is None:
                print("DESCRIPTION IS NONE FOR SOME REASON???")
                return
            
            print("welcome to [dank memer]" in desc, "welcome to" in desc)

            if "you leveled up" in desc:
                new_level = re.findall(r'\d+', desc.split('\n')[1])[1]
                print('NEW USER LEVEL IS:', new_level)
            elif "welcome to [dank memer]" in desc:
                # New account
                print("NEW ACCOUNT DETECTED")
            else:
                print('Received a DM from Dank Memer:')
                print(title)
                print(desc)

    @staticmethod
    async def safe_delay(min_delay=0.5, max_delay=1):
        await asyncio.sleep(round(random.uniform(min_delay, max_delay), 2))

    async def select_option(self, msg, comp_num, val):
        # Select an option in a select menu
        # Can select by using either the option index or option name
        comp = msg.components[comp_num]

        await self.safe_delay()

        if isinstance(val, int):
            options = comp.children[0].options
            if len(options) > val:
                await comp.children[0].choose(options[val])
        elif isinstance(val, str):
            for option in comp.children[0].options:
                if option.label.lower() == val.lower():
                    await comp.children[0].choose(option)

    async def click(self, msg, comp_num, btn_val):
        # Click a button by it's index
        await self.safe_delay()

        if not len(msg.components) > comp_num:
            print('IndexError, that component doesnt exist...')
            return
        comp = msg.components[comp_num]

        comp_btn = None

        if isinstance(btn_val, int):
            if not len(comp.children) > btn_val:
                print('IndexError, child of button component doesnt exist...')
                return
            
            comp_btn = comp.children[btn_val]

        if isinstance(btn_val, str):
            # search through the buttons to find it
            possible = []
            for btn_index, btn in enumerate(comp.children):
                possible.append(btn.label.lower())
                if btn.label.lower() == btn_val.lower():
                    comp_btn = comp.children[btn_index]
                    break
            if comp_btn is None:
                #### TESTING
                print(f"{btn_val} was not found in {possible}")
                return False

        # elif isinstance(btn_val, str):
        
        for x in range(10):
            try:
                await comp_btn.click()
            except discord.errors.HTTPException as e:
                if 'COMPONENT_VALIDATION_FAILED' in str(e):
                    print('component_validation_failed!')
            except Exception as e:
                print(f"Error while trying to click the button: {e}")
                await asyncio.sleep(1)
                continue
            else:
                return True
            
            if comp_btn.disabled == True:
                print('button disabled!')
                return True
            
            if comp.children is None:
                print('comp.children is none bruh')
                return True

            
        print('Clicking button didnt work after 10 TRIES HOLY!!!!!!')
    
    @staticmethod
    async def submit_modal(modal, answer):
        input = modal.components[0].children[0]
        input.answer(str(answer))
        await modal.submit()
    
    @staticmethod
    def get_coins_from_text(text):
        match_coins = re.search(r'\u23e3 (\d{1,3}(?:,\d{3})*)', text)
        if match_coins:
            coins = match_coins.group(1).replace(',', '')
            return int(coins)
        
    @staticmethod
    def get_rewards_from_text(text):
        item_pattern = re.compile(r'(\d+) <:[^:]+:\d+> (\w+)')
        coins_pattern = re.compile(r'\u23e3 ([\d,]+)')
        
        items = {}
        for match in item_pattern.findall(text):
            quantity, item = int(match[0]), match[1].lower()
            if item in items:
                items[item] += quantity
            else:
                items[item] = quantity
                
        coins_match = coins_pattern.search(text)
        coins = int(coins_match.group(1).replace(',', '')) if coins_match else None
        
        return items if items else None, coins

    @staticmethod
    def get_item_from_text(text):
        match_item = re.match(r'^.*?\s(\d+)\s<.*?>\s(.+)$', text)
        if match_item:
            amount = match_item.group(1)
            item_name = match_item.group(2)
            return int(amount), item_name
        return None, None
    
    @staticmethod
    def get_item_from_text2(text):
        match_item = re.match(r'^.*?\*\*(\d+)\s<:[^:]+:\d+>\s(.+?)\s+and\s+\\u23e3\s([\d,]+)\*\*!$', text)
        if match_item:
            amount = match_item.group(1)
            item_name = match_item.group(2)
            points = match_item.group(3)
            return int(amount), item_name, points
        return None, None, None

    @staticmethod
    def check_cooldown(msg):
        return "cooldown is" in msg.embeds[0].description

    async def auto_farm(self):
        # Managing the farming for the bot

        # self.buy_item = self.cmds['buyitem']['run']
        # await self.buy_item('hunting rifle', 1)

        print('Starting autofarm...')
        # await self.cmds['postmemes']['run']()

        # Scrape inventory !!
        # inv = await self.cmds['getinventory']['run']()
        # print(inv)