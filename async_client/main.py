#!/usr/bin/env python3
import os
import logging
import asyncio
import aiohttp
import json
import sys
import functools
from solver_client import solver_client

logger = logging.getLogger()

# read a file and despatch a 1000 lines at a time to wordament.  
MAX_WORD_LOAD = 1000
tasks = []

# Using asyncio to prevent input() from blocking.  
# https://stackoverflow.com/questions/35223896/listen-to-keypress-with-asyncio
class Prompt:
    def __init__(self, loop=None):
        self.loop = loop or asyncio.get_event_loop()
        self.q = asyncio.Queue(loop=self.loop)
        self.loop.add_reader(sys.stdin, self.got_input)

    def got_input(self):
        asyncio.ensure_future(self.q.put(sys.stdin.readline()), loop=self.loop)

    async def __call__(self, msg, end='\n', flush=False):
        print(msg, end=end, flush=flush)
        return (await self.q.get()).rstrip('\n')

prompt = Prompt()
raw_input = functools.partial(prompt, end='', flush=True)



async def main(base_url: str):
    # We use only one session
    async with aiohttp.ClientSession() as session:
        while True:
            client = solver_client(session, base_url, MAX_WORD_LOAD)

            # Use health endpoint to get data
            response = await client.get_health()
            logging.info(response)

            response = await client.dictionary_names()
            logger.info(response)             

            name = ""
            while name == "": 
                name = await raw_input("Dictionary name (quit):")
            
            if name.lower() == "quit":
                break

            response = await client.dictionary_stat(name)
            logger.info(response) 
            
            # hard coded value for number of words in dictionary file
            if response[0] != 200 or response[1]["num_of_words"] < 370103:
                # create dictionary is idempotent
                response = await client.create_dictionary(name)
                logger.info(response)

                # build the dictionary async
                build_dictionary_task = asyncio.create_task(client.build_dictionary("../test_data/words_alpha.txt", name))

            grid = await raw_input("Enter grid or (quit) - examples 'GLNTSRAWRPHSEOPS':")
            if grid.lower() == "quit":
                break
            else:
                if grid == "":
                    grid = 'GLNTSRAWRPHSEOPS'

                task = asyncio.create_task(client.solve(grid, name))
                logger.debug(f"wait on solve task - {id(task)}")
                response = await task  
                logger.info(response)

            #all_tasks = asyncio.all_tasks()
            #logging.info(all_tasks)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    base_url = "http://localhost:8000/api"
    if 'SERVER_URL' in os.environ:
        base_url = os.environ['SERVER_URL']

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(base_url))
    loop.close()
