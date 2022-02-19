import asyncio
import multiprocessing
import numpy
import random
import json
import sys
import readchar
import time
import marshal
import pickle

import threading

import roblox
from roblox import Client
from queue import Queue
import concurrent.futures as cf#import ThreadPoolExecutor, as_completed

from utils import Colors
from utils import Style, Back
from utils import Textual
from utils import Auth
from utils import AuthCookie


class App:
    def __init__(self, **kwargs):
        self.client = kwargs['client']
        self._group = kwargs['group']
        self._exceptions = kwargs['exceptions']
        self.client_rank = None
        self._members = []
        self._scrambled = {}
        self.mcnt = 0
    
    async def init_core(self):
        Textual.log('Loading Group...', type=Colors.information())
        self._group = await self.client.get_group(self._group)

        client_partial = await self.client.get_authenticated_user()
        self.client_rank = await self._group.get_member_rank(client_partial.id)

        roles = await self._group.get_roles()
        for role in roles:
            if role.name == self.client_rank.name or role.name == '[LCPL] Lance Corporal':
                break
            if role.name == 'Guest':
                continue
            self._scrambled[role.id] = [[], role]
            self.mcnt += role.member_count

        Textual.del_lines(1)
        Textual.log(f'Fetched Group Object for {Back.GREEN}{self._group.name}', type=Colors.information())
        
    async def get_group_members(self):
        members = self._group.get_members(page_size=100, sort_order=roblox.utilities.iterators.SortOrder.Descending)
        Textual.log(f'Loading Member Objects...', type=Colors.information())
        it_n = 0
        async for page in members.pages():
            for member in page:
                if member.role.rank < self.client_rank.rank and member.name not in self._exceptions:
                    Textual.del_lines(1)
                    it_n += 1
                    self._members.append(member)
                    Textual.log(f'Initialising Member Object {Back.MAGENTA}{round((it_n/self.mcnt) * 100)}%{Back.RESET} {Back.RED}{"".join(member.role.name.split("]")[0])}] {member.name.upper()}{Back.RESET}', type=Colors.information())

        Textual.del_lines(1)
        Textual.log(f'Initialised {Back.GREEN}{len(self._members)}{Back.RESET} Member Objects', type=Colors.information())

    async def batch_scramble(self):
        Textual.log(f'Scrambling Objects Into Batches...', type=Colors.information())
        random.shuffle(self._members)
        keys = [*self._scrambled]
        _scrambled = numpy.array_split(self._members, len(keys))
        itr_v = -1
        for lst in _scrambled:
            itr_v += 1
            try:
                self._scrambled[keys[itr_v]][0] = list(lst).remove('r')
            except:
                self._scrambled[keys[itr_v]][0] = list(lst)

            Textual.del_lines(1)
            Textual.log(f'Scrambling Objects Into Batches {Back.MAGENTA}{round(itr_v/len(keys) * 100)}%', type=Colors.information())
            await asyncio.sleep(1)

        Textual.del_lines(1)
        Textual.log(f'Scrambled Objects Into {Back.GREEN}{len(keys)}{Back.RESET} Batches', type=Colors.information())

    async def conf_dump(self):
        Textual.log(f'Press Any Key To Begin Admin Abuse...', type=Colors.information())
        readchar.readchar()
        Textual.del_lines(1)

    async def mass_dump(self):
        Textual.log(f'Beginning Mass Rank Dump...', type=Colors.information())
        keys = [*self._scrambled]

        async def internal(*args):
            itr_v = -1
            _futures = []
            for obj in self._scrambled[args[0]][0]:
                itr_v += 1
                Textual.del_lines(1)
                Textual.log(f'Begun Mass Rank Dump {Back.MAGENTA}Batch {args[1]}/{len(args[2])}{Back.RESET} {Back.YELLOW}{round(itr_v/len(self._scrambled[args[0]][0]) * 100)}%{Back.RESET} {Back.RED}[{obj.role.name}] {obj.name.upper()} >>> {self._scrambled[batch][1].name}{Back.RESET}', type=Colors.information())
                task = asyncio.ensure_future(obj.set_role(args[0]))
                _futures.append(task)
            await asyncio.gather(*_futures)
            
        _tick = time.perf_counter()
        itr_bat = 0
        futures = []
        # print(keys)
        # await asyncio.sleep(20)
        for batch in keys:
            itr_bat += 1
            task = asyncio.ensure_future(internal(batch, itr_bat, keys))
            futures.append(task)

        Textual.log(f'Waiting for futures...', type=Colors.information())
        # await asyncio.gather(*futures)
        tick = round(time.perf_counter() - _tick, 2)
        Textual.del_lines(5)
        Textual.log(f'Completed Admin Abuse for {Back.GREEN}{self._group.name}{Back.RESET}', type=Colors.information())
        Textual.log(f'Ranked {Back.MAGENTA}{len(self._members)} Users{Back.RESET}', type=Colors.information())
        Textual.log(f'Through {Back.MAGENTA}{len(keys)} Batches{Back.RESET}', type=Colors.information())
        Textual.log(f'Completed in {Back.YELLOW}{tick} Seconds{Back.RESET}', type=Colors.information())


if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    auth = Auth(Client(), product_name='Test', hub_id='fvOu062RQw')
    _client = AuthCookie()

    app = App(
        client=_client.client,
        # group=13183519,
        group=11908206,
        exceptions=['RescueHolder', '1vs_4w', 'Justinkiller1221']
        )

    loop.run_until_complete(app.init_core())
    loop.run_until_complete(app.get_group_members())
    loop.run_until_complete(app.batch_scramble())
    loop.run_until_complete(app.conf_dump())
    loop.run_until_complete(app.mass_dump())

