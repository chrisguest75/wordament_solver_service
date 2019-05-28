#!/usr/bin/env python3
import os
import logging
import asyncio
import aiohttp
import aiofiles
import json
import sys
import functools

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


async def create_dictionary(session, base_url: str, name:str): 
    """ Create an empty dictionary on the server 
    """
    url = f"{base_url}/dictionary/{name}"
    logger.debug(f"create_dictionary {url}")
    async with session.post(url, data="[]", headers={'content-type': 'application/json'}) as response:
        response_json = await response.json()
        return response.status, response_json


async def add_to_dictionary(session, base_url: str, name:str, words):
    """ Add an array of words to the dictionary
    """
    url = f"{base_url}/dictionary/{name}"
    logger.debug(f"add_to_dictionary {url}")
    async with session.put(url, data=json.dumps(words), headers={'content-type': 'application/json'}) as response:
        response_json = await response.json()
        return response.status, response_json


async def build_dictionary(session, base_url: str, name:str):
    """ Build the dictionary using asynchronous tasks. 
    NOTE: It only despatches one request at a time.   
    """
    async with aiofiles.open("../test_data/words_alpha.txt") as f:
        lines = []
        async for line in f:
            lines.append(line.strip())
            if (len(lines) == MAX_WORD_LOAD):
                task = asyncio.create_task(add_to_dictionary(session, base_url, name, lines))
                logger.debug(f"wait on task - {id(task)} for {name}")
                response = await task     
                logger.debug("building dictionary response {}".format(response))
                lines = []

        # do remaining words
        if len(lines) > 0: 
            task = asyncio.create_task(add_to_dictionary(session, base_url, name, lines))    
            logger.debug(f"wait on task - {id(task)} for {name}")
            response = await task   
            logger.debug(f"dictionary response {response}")


async def solve(session, base_url: str, grid: str, name:str):
    """ Solve the grid with the named dictionary 
    """
    url = (f"{base_url}/puzzle/solve/{grid}?dictionary_id={name}")
    async with session.get(url) as response:
        response_json = await response.json()
        return response.status, response_json


async def get_health(session, base_url: str):
    """ Get health endpoint 
    """
    url = f"{base_url}/health"
    async with session.get(url) as response:
        response_json = await response.json()
        return response.status, response_json


async def dictionary_stat(session, base_url: str, name:str):
    """ Get statistics for the dictionary 
    """
    url = f"{base_url}/dictionary/{name}"
    async with session.get(url) as response:
        response_json = await response.json()
        return response.status, response_json

async def dictionary_names(session, base_url: str):
    """ Get the names of the dictionaries stored on the server    
    """
    url = f"{base_url}/dictionary"
    async with session.get(url) as response:
        response_json = await response.json()
        return response.status, response_json

async def main(base_url: str):
    # We use only one session
    async with aiohttp.ClientSession() as session:
        while True:
            # Use health endpoint to get data
            response = await get_health(session, base_url)
            logging.info(response)

            response = await dictionary_names(session, base_url)
            logger.info(response)             

            name = ""
            while name == "": 
                name = await raw_input("Dictionary name (quit):")
            
            if name.lower() == "quit":
                break

            response = await dictionary_stat(session, base_url, name)
            logger.info(response) 
            
            # hard coded value for number of words in dictionary file
            if response[0] != 200 or response[1]["num_of_words"] < 370103:
                # create dictionary is idempotent
                response = await create_dictionary(session, base_url, name)
                logger.info(response)

                # build the dictionary async
                build_dictionary_task = asyncio.create_task(build_dictionary(session, base_url, name))

            grid = await raw_input("Enter grid or (quit) - examples 'GLNTSRAWRPHSEOPS':")
            if grid.lower() == "quit":
                break
            else:
                if grid == "":
                    grid = 'GLNTSRAWRPHSEOPS'

                task = asyncio.create_task(solve(session, base_url, grid, name))
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
