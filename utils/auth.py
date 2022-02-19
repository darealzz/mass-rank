from typing import Text
import aiohttp
import asyncio
import roblox
from roblox import Client
import random
import sys
import os

import nest_asyncio
nest_asyncio.apply()

from .data import Data
from .textual import Textual
from .types import Colors
from .types import Back
from .types import Keys

class Auth:
    def __init__(self, *args, **kwargs):
        self.client = args[0]
        self.product_name = kwargs['product_name']
        self.hub_id = kwargs['hub_id']
        self.mediate = ' '.join([random.choice(('blue', 'red', 'green', 'pink', 'orange', 'purple', 'cat', 'dog', 'this', 'board', 'game')) for w in range(5)])

        loop = asyncio.get_event_loop()

        is_allwed = loop.run_until_complete(self.pre_check())
        if is_allwed:
            return

        while True:
            success = loop.run_until_complete(self.take_username())
            if success:
                break

        loop.run_until_complete(self.has_product())
        loop.run_until_complete(self.mediate_blurb())
        loop.run_until_complete(self.dump_data())


    async def pre_check(self):
        data = await Data.get_data(Keys.user_id)
        if data:
            self.user_id = data
            self.has_product()
            loop = asyncio.get_event_loop()
            Textual.log(f'Hey {Back.MAGENTA}{loop.run_until_complete(self.client.get_user(int(data))).display_name}{Back.RESET}, sit tight whilst we get everything loaded...', type=Colors.information())
            await asyncio.sleep(2)
            return True

    async def take_username(self):
        loop = asyncio.get_event_loop()
        username = Textual.take_inptut(f'Please enter your ROBLOX username:', type=Colors.take(), cls=True)
        Textual.log(f'Authenticating Roblox Oject...', type=Colors.take_info())

        await asyncio.sleep(1)

        try:
            self._user = loop.run_until_complete(self.client.get_user_by_username(username))
            self.user_id = self._user.id
            return True
        except:
            Textual.del_lines(1)
            Textual.log(f'This account does not exist, please enter a new username', type=Colors.information())
            await asyncio.sleep(2)
            return None

    async def has_product(self):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f'http://api.onpointrblx.com/vendr/v1/licences/getlicence/{self.hub_id}/roblox/{self.user_id}/?productName={self.product_name}') as r:                    
                if r.status == 404:
                    Textual.log(f'This account does not have a license', type=Colors.information())
                    sys.exit()

    async def mediate_blurb(self):
        Textual.del_lines(2)
        Textual.log(f'Please change your description to {Back.MAGENTA}{self.mediate}', type=Colors.information())
        Textual.log(f'Waiting for authenticated description...', type=Colors.information())

        d_cnt = 3
        while True:
            if self._user.description.lower() != self.mediate:
                self._user = await self._user.regen_user()

                await asyncio.sleep(1)
                Textual.del_lines(1)
                d_cnt += -2 if d_cnt == 3 else 1
                Textual.log(f'Waiting for authenticated description{"." * d_cnt}', type=Colors.information())

                continue
            break

    async def dump_data(self):
        data = await Data.dump_data(Keys.user_id, self.user_id)
        
class AuthCookie:
    def __init__(self):
        loop = asyncio.get_event_loop()

        while True:
            success = loop.run_until_complete(self.take_cookie())
            if success:
                while True:
                    confirm = loop.run_until_complete(self.confirm_cookie())
                    if confirm:
                        break
                    if confirm == False:
                        break
                if confirm:
                    break

        os.system('cls')
        loop.run_until_complete(self.dump_data())

    async def take_cookie(self):
        loop = asyncio.get_event_loop()
        cookie = Textual.take_inptut(f'Please provide the Abuse Account Cookie:', type=Colors.take(), cls=True)
        Textual.log(f'Authenticating Roblox Oject...', type=Colors.take_info())

        await asyncio.sleep(1)

        try:
            self.cookie = cookie
            self.client = Client(self.cookie)
            self._user = loop.run_until_complete(self.client.get_authenticated_user())
            return True
        except:
            Textual.del_lines(1)
            Textual.log(f'This Cookie is not valid, please enter a new cookie', type=Colors.information())
            await asyncio.sleep(2)
            return None

    async def confirm_cookie(self):
        loop = asyncio.get_event_loop()
        os.system('cls')

        Textual.log(f'Account Details - {self._user.name} {Back.MAGENTA}({self._user.id}){Back.RESET}', type=Colors.information())
        confirm = Textual.take_inptut(f'Confirm the account [YES/NO]:', type=Colors.take(), cls=False).strip().lower()
        if confirm in ('yes', 'ye', 'y', 'yea'):
            Textual.del_lines(1)
            return True
        elif confirm in ('no', 'n', 'nah', 'nope'):
            Textual.log(f'Refreshing Prompt...', type=Colors.take_info())
            await asyncio.sleep(2)
            Textual.del_lines(2)
            return False
        else:
            Textual.log(f'Please provide a valid input [YES/NO]', type=Colors.information())
            await asyncio.sleep(2)
            Textual.del_lines(2)
            return None

    async def dump_data(self):
        data = await Data.dump_data(Keys.cookie, self.cookie)
